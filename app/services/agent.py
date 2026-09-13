"""AI Agent service with tool calling for business operations."""
import json
import logging
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import ollama
from sqlalchemy.orm import Session

from app.models.database import Business, Service, FAQ, Appointment, Lead
from config import settings

logger = logging.getLogger(__name__)


# Tool definitions for function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check if a service is available at a given time slot",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "string", "description": "ID of the service"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Time in HH:MM format"}
                },
                "required": ["service_id", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                    "customer_phone": {"type": "string"},
                    "customer_email": {"type": "string"},
                    "service_id": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["customer_name", "customer_phone", "service_id", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancel an existing appointment",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["appointment_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_business_info",
            "description": "Get business information like hours, location, services",
            "parameters": {
                "type": "object",
                "properties": {
                    "info_type": {"type": "string", "enum": ["hours", "location", "services", "contact", "all"]}
                },
                "required": ["info_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_faqs",
            "description": "Search FAQ database for relevant answers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The question or topic"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_lead",
            "description": "Create or update a lead from a call",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "notes": {"type": "string"},
                    "source": {"type": "string"}
                },
                "required": ["name", "phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "Request transfer to a human agent",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]}
                }
            }
        }
    }
]


class ReceptionistAgent:
    """
    AI Receptionist Agent that handles phone calls for businesses.
    
    This agent uses tool calling to perform real business actions:
    - Check availability
    - Book/cancel appointments
    - Answer FAQs
    - Capture leads
    - Transfer to humans
    """
    
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}  # session_id -> conversation history
        self.tool_registry: Dict[str, callable] = {
            'check_availability': self._handle_check_availability,
            'book_appointment': self._handle_book_appointment,
            'cancel_appointment': self._handle_cancel_appointment,
            'get_business_info': self._handle_get_business_info,
            'search_faqs': self._handle_search_faqs,
            'create_lead': self._handle_create_lead,
            'transfer_to_human': self._handle_transfer_to_human,
        }
    
    async def _call_tool(self, tool_name: str, tool_input: Dict[str, Any], 
                         db_session: Session, business: Business) -> Dict[str, Any]:
        """Execute a tool and return results."""
        handler = self.tool_registry.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            result = await handler(tool_input, db_session, business)
            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_check_availability(self, params: Dict, db: Session, business: Business) -> Dict:
        """Check service availability."""
        service_id = params.get('service_id')
        date = params.get('date')
        time = params.get('time')
        
        # Query existing appointments to check conflicts
        existing = db.query(Appointment).filter(
            Appointment.business_id == business.id,
            Appointment.status.in_(['confirmed', 'pending']),
            Appointment.start_time >= f"{date}T{time}",
            Appointment.start_time <= f"{date}T{time}:59"
        ).all()
        
        is_available = len(existing) == 0
        return {
            "available": is_available,
            "slot": f"{date} {time}",
            "conflicting_appointments": len(existing)
        }
    
    async def _handle_book_appointment(self, params: Dict, db: Session, business: Business) -> Dict:
        """Book a new appointment."""
        from app.models.database import Appointment
        
        # Validate inputs
        required = ['customer_name', 'customer_phone', 'service_id', 'date', 'time']
        for field in required:
            if field not in params or not params[field]:
                return {"success": False, "error": f"Missing required field: {field}"}
        
        # Parse date/time
        try:
            start_dt = datetime.fromisoformat(f"{params['date']}T{params['time']}")
            duration_minutes = 30  # Default duration
            end_dt = start_dt.replace(minute=(start_dt.minute + duration_minutes) % 60,
                                      hour=start_dt.hour + (start_dt.minute + duration_minutes) // 60)
        except ValueError as e:
            return {"success": False, "error": f"Invalid date/time format: {e}"}
        
        # Check availability first
        availability = await self._handle_check_availability(
            {'service_id': params['service_id'], 'date': params['date'], 'time': params['time']},
            db, business
        )
        
        if not availability.get('available'):
            return {"success": False, "error": "Time slot not available"}
        
        # Create appointment
        appointment = Appointment(
            business_id=business.id,
            title=params.get('title'),
            description=params.get('notes'),
            customer_name=params['customer_name'],
            customer_phone=params['customer_phone'],
            customer_email=params.get('customer_email'),
            start_time=start_dt,
            end_time=end_dt,
            status='confirmed'
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        
        return {
            "success": True,
            "appointment_id": str(appointment.id),
            "confirmation": f"Appointment booked for {appointment.customer_name} on {appointment.start_time}"
        }
    
    async def _handle_cancel_appointment(self, params: Dict, db: Session, business: Business) -> Dict:
        """Cancel an appointment."""
        from app.models.database import Appointment
        
        appointment_id = params.get('appointment_id')
        if not appointment_id:
            return {"success": False, "error": "Missing appointment_id"}
        
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id,
            Appointment.business_id == business.id
        ).first()
        
        if not appointment:
            return {"success": False, "error": "Appointment not found"}
        
        appointment.status = 'cancelled'
        appointment.updated_at = datetime.utcnow()
        db.commit()
        
        return {"success": True, "message": "Appointment cancelled successfully"}
    
    async def _handle_get_business_info(self, params: Dict, db: Session, business: Business) -> Dict:
        """Get business information."""
        info_type = params.get('info_type', 'all')
        config = business.business_config or {}
        
        result = {"business_name": business.name}
        
        if info_type in ['hours', 'all']:
            result['hours'] = config.get('business_hours', 'Mon-Fri 9am-5pm')
        if info_type in ['location', 'all']:
            result['location'] = config.get('address', 'Contact business for location')
        if info_type in ['contact', 'all']:
            result['phone'] = config.get('contact_phone', 'N/A')
            result['email'] = config.get('contact_email', 'N/A')
        if info_type in ['services', 'all']:
            services = db.query(Service).filter(
                Service.business_id == business.id,
                Service.available == True
            ).all()
            result['services'] = [{
                "id": str(s.id),
                "name": s.name,
                "duration": s.duration_minutes,
                "price": s.price
            } for s in services]
        
        return result
    
    async def _handle_search_faqs(self, params: Dict, db: Session, business: Business) -> Dict:
        """Search FAQ database."""
        from app.models.database import FAQ
        
        query = params.get('query', '').lower()
        
        # Simple keyword matching (could be enhanced with embeddings)
        faqs = db.query(FAQ).filter(
            FAQ.business_id == business.id,
            FAQ.answer.contains(query) | FAQ.question.contains(query)
        ).limit(5).all()
        
        return {
            "results": [
                {"question": f.qestion, "answer": f.answer}
                for f in faqs
            ]
        }
    
    async def _handle_create_lead(self, params: Dict, db: Session, business: Business) -> Dict:
        """Create or update a lead."""
        from app.models.database import Lead
        
        lead = Lead(
            business_id=business.id,
            name=params.get('name'),
            phone_number=params.get('phone'),
            email=params.get('email'),
            notes=params.get('notes'),
            source=params.get('source', 'phone_call')
        )
        
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        return {
            "success": True,
            "lead_id": str(lead.id),
            "message": f"Lead created for {lead.name}"
        }
    
    async def _handle_transfer_to_human(self, params: Dict, db: Session, business: Business) -> Dict:
        """Handle transfer to human."""
        config = business.business_config or {}
        transfer_number = config.get('transfer_phone', 'Not configured')
        
        return {
            "success": True,
            "message": "Transferring to human agent...",
            "transfer_number": transfer_number,
            "priority": params.get('priority', 'medium')
        }
    
    async def get_response(self, 
                          session_id: str,
                          user_message: str,
                          db_session: Session,
                          business: Business,
                          caller_number: str = None) -> Dict[str, Any]:
        """
        Get AI response for a call session.
        
        Returns dict with:
        - text: Response text
        - tools: Tools called during response
        - should_transfer: Boolean flag for human transfer
        """
        # Initialize conversation if new
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            
            # Build system prompt with business context
            config = business.business_config or {}
            services = db_session.query(Service).filter(
                Service.business_id == business.id
            ).all()
            faqs = db_session.query(FAQ).filter(
                FAQ.business_id == business.id
            ).limit(10).all()
            
            system_prompt = self._build_system_prompt(business, services, faqs, config)
            self.conversations[session_id].append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add user message
        self.conversations[session_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Keep conversation manageable
        if len(self.conversations[session_id]) > 20:
            self.conversations[session_id] = [
                self.conversations[session_id][0],
                *self.conversations[session_id][-18:]
            ]
        
        try:
            # Call Ollama with tool definitions
            response = ollama.chat(
                model=settings.OLLAMA_MODEL,
                messages=self.conversations[session_id],
                tools=TOOL_DEFINITIONS,
                stream=False
            )
            
            ai_message = response['message']
            response_text = ai_message.get('content', '')
            tool_calls = ai_message.get('tool_calls', [])
            
            # Process tool calls
            tool_results = []
            should_transfer = False
            
            for tool_call in tool_calls:
                func = tool_call['function']
                name = func['name']
                arguments = json.loads(func['arguments'])
                
                # Execute tool
                result = await self._call_tool(name, arguments, db_session, business)
                tool_results.append({
                    "tool": name,
                    "input": arguments,
                    "output": result
                })
                
                # Add tool result to conversation
                self.conversations[session_id].append({
                    "role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": json.dumps(result)
                })
                
                # Check if transfer requested
                if name == 'transfer_to_human':
                    should_transfer = True
            
            # If tools were called, get follow-up response
            if tool_results:
                follow_up = ollama.chat(
                    model=settings.OLLAMA_MODEL,
                    messages=self.conversations[session_id],
                    stream=False
                )
                response_text = follow_up['message'].get('content', response_text)
            
            # Clean up conversation (remove tool messages, keep essential history)
            self.conversations[session_id] = [
                msg for msg in self.conversations[session_id]
                if msg['role'] != 'tool'
            ][:10]  # Keep last 10 messages
            
            return {
                "text": response_text,
                "tools_called": tool_results,
                "should_transfer": should_transfer,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Agent error: {e}")
            return {
                "text": "I'm sorry, I'm having trouble processing your request. Let me connect you with someone.",
                "tools_called": [],
                "should_transfer": True,
                "session_id": session_id,
                "error": str(e)
            }
    
    def _build_system_prompt(self, business: Business, services: list, faqs: list, config: dict) -> str:
        """Build system prompt with business context."""
        prompt = f"""You are a professional AI voice receptionist for {business.name}.

BUSINESS INFORMATION:
- Name: {business.name}
- Description: {business.description or 'A local business'}
- Timezone: {business.timezone}
- Language: {business.language}

BUSINESS HOURS:
{config.get('business_hours', 'Monday-Friday 9AM-5PM')}

LOCATION:
{config.get('address', 'Contact business for location')}

CONTACT:
Phone: {config.get('contact_phone', 'N/A')}
Email: {config.get('contact_email', 'N/A')}
"""
        
        if services:
            prompt += "\nSERVICES:\n"
            for s in services[:10]:
                prompt += f"- {s.name} ({s.duration_minutes} min)"
                if s.price:
                    prompt += f" - ${s.price}"
                prompt += "\n"
        
        if faqs:
            prompt += "\nKNOWLEDGE BASE (FAQs):\n"
            for f in faqs[:5]:
                prompt += f"Q: {f.question}\nA: {f.answer}\n\n"
        
        prompt += """
YOUR RESPONSIBILITIES:
1. Answer caller questions professionally and concisely
2. Use tools to check availability and book appointments
3. Capture lead information when appropriate
4. Transfer to human when needed (unclear requests, urgent matters, complaints)
5. NEVER make up information about prices, availability, or policies
6. ALWAYS confirm important details before booking
7. Be warm, helpful, and efficient

CONVERSATION GUIDELINES:
- Ask one question at a time
- Confirm understanding before proceeding
- Use natural, conversational language
- Keep responses concise (under 2-3 sentences typically)
- If unsure, say so and offer to transfer

ESCALATION TRIGGERS (use transfer_to_human tool):
- Customer complaint or dissatisfaction
- Technical issues they can't resolve
- Urgent/emergency requests
- Complex questions you can't answer confidently
- Request to speak to a real person

Remember: You are representing {business.name}. Be professional and helpful.
"""
        return prompt
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history."""
        if session_id in self.conversations:
            del self.conversations[session_id]


# Global agent instance
agent = ReceptionistAgent()