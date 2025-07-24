# CapeAI Backend Service Implementation

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from openai import AsyncOpenAI
import redis
import json
import uuid
from datetime import datetime
import asyncio

from app.dependencies import get_current_user
from app.models import User
from app.config import settings

router = APIRouter(prefix="/ai", tags=["CapeAI"])

# Redis connection for conversation memory
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

# OpenAI client
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AIPromptRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    session_id: str
    context: Dict[str, Any]
    suggestions: List[str] = []
    actions: List[Dict[str, str]] = []

class CapeAIService:
    """Core CapeAI service for intelligent user assistance"""
    
    def __init__(self):
        self.conversation_cache = {}
        self.user_profiles = {}
        
    async def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve conversation history from Redis"""
        try:
            history_key = f"cape_ai:conversation:{session_id}"
            messages = redis_client.lrange(history_key, -limit, -1)
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []
    
    async def save_conversation(self, session_id: str, message: Dict[str, Any]):
        """Save conversation message to Redis"""
        try:
            history_key = f"cape_ai:conversation:{session_id}"
            redis_client.lpush(history_key, json.dumps(message))
            redis_client.expire(history_key, 86400 * 7)  # 7 days
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    async def analyze_user_context(self, user: User, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user context for personalized responses"""
        
        # Current page context
        current_page = context.get('currentPath', '/')
        onboarding_step = context.get('onboardingStep', 0)
        user_role = getattr(user, 'role', 'user')
        
        # Determine user expertise level
        account_age_days = (datetime.now() - user.created_at).days if hasattr(user, 'created_at') else 0
        expertise_level = 'beginner' if account_age_days < 7 else 'intermediate' if account_age_days < 30 else 'advanced'
        
        return {
            'current_page': current_page,
            'onboarding_step': onboarding_step,
            'user_role': user_role,
            'expertise_level': expertise_level,
            'account_age_days': account_age_days,
            'platform_context': self._get_platform_context(current_page)
        }
    
    def _get_platform_context(self, path: str) -> Dict[str, Any]:
        """Get platform-specific context based on current path"""
        
        platform_contexts = {
            '/': {
                'area': 'landing',
                'primary_actions': ['explore_features', 'start_onboarding'],
                'help_topics': ['getting_started', 'platform_overview']
            },
            '/dashboard': {
                'area': 'dashboard',
                'primary_actions': ['view_analytics', 'manage_agents'],
                'help_topics': ['dashboard_navigation', 'key_metrics']
            },
            '/agents': {
                'area': 'agents',
                'primary_actions': ['browse_agents', 'install_agent'],
                'help_topics': ['agent_selection', 'agent_configuration']
            },
            '/profile': {
                'area': 'profile',
                'primary_actions': ['update_profile', 'configure_preferences'],
                'help_topics': ['account_settings', 'billing_management']
            }
        }
        
        # Find matching context or default
        for pattern, context in platform_contexts.items():
            if path.startswith(pattern):
                return context
                
        return platform_contexts['/']  # Default to landing context
    
    async def generate_contextual_response(
        self, 
        message: str, 
        user_context: Dict[str, Any], 
        conversation_history: List[Dict]
    ) -> Dict[str, Any]:
        """Generate AI response using OpenAI with context awareness"""
        
        # Build context-aware system prompt
        system_prompt = self._build_system_prompt(user_context)
        
        # Prepare conversation messages for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        try:
            # Call OpenAI API
            response = await openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            
            # Generate contextual suggestions and actions
            suggestions = self._generate_suggestions(user_context, message)
            actions = self._generate_actions(user_context, ai_response)
            
            return {
                "response": ai_response,
                "suggestions": suggestions,
                "actions": actions,
                "context": user_context
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback response
            return self._generate_fallback_response(message, user_context)
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build context-aware system prompt for OpenAI"""
        
        base_prompt = """You are CapeAI, an intelligent assistant for the CapeControl platform - a professional AI-agents marketplace and automation platform.

Your personality: Helpful, professional, concise, and encouraging. You understand both technical and business aspects of AI automation.

Your role: Guide users through the platform, provide intelligent suggestions, help with onboarding, and assist with AI agent selection and management."""

        # Add context-specific guidance
        current_area = context.get('platform_context', {}).get('area', 'general')
        expertise_level = context.get('expertise_level', 'beginner')
        
        context_prompts = {
            'landing': "The user is on the landing page. Focus on explaining CapeControl's value proposition and guiding them to get started.",
            'dashboard': "The user is viewing their dashboard. Help them understand metrics, suggest optimizations, and guide them to relevant features.",
            'agents': "The user is in the AI agents section. Help them discover, evaluate, and configure AI agents that match their needs.",
            'profile': "The user is managing their profile/settings. Assist with account configuration and preference optimization."
        }
        
        expertise_guidance = {
            'beginner': "Provide step-by-step guidance and explain concepts clearly. Focus on fundamental features first.",
            'intermediate': "Assume basic platform knowledge. Provide actionable advice and intermediate optimization tips.",
            'advanced': "Focus on advanced features, efficiency improvements, and strategic recommendations."
        }
        
        full_prompt = f"""{base_prompt}

CURRENT CONTEXT: {context_prompts.get(current_area, 'General platform assistance')}

USER EXPERTISE: {expertise_guidance.get(expertise_level, 'Adapt to user needs')}

GUIDELINES:
- Keep responses concise but helpful (2-3 sentences max)
- Always provide actionable next steps when possible  
- If asked about features, explain benefits and guide to relevant sections
- For technical questions, provide clear explanations appropriate to user expertise level
- Suggest relevant AI agents when discussing automation needs"""

        return full_prompt
    
    def _generate_suggestions(self, context: Dict[str, Any], message: str) -> List[str]:
        """Generate contextual suggestions based on user context and message"""
        
        platform_context = context.get('platform_context', {})
        area = platform_context.get('area', 'general')
        
        # Context-specific suggestions
        suggestions_map = {
            'landing': [
                "Start your onboarding journey",
                "Explore AI agent marketplace", 
                "View platform demo"
            ],
            'dashboard': [
                "Check your usage analytics",
                "Optimize your AI agents",
                "Review cost breakdown"
            ],
            'agents': [
                "Browse trending AI agents",
                "Filter agents by category",
                "Compare agent pricing"
            ],
            'profile': [
                "Update billing preferences",
                "Configure notification settings",
                "Review security settings"
            ]
        }
        
        base_suggestions = suggestions_map.get(area, ["How can I help you today?"])
        
        # Add message-specific suggestions
        message_lower = message.lower()
        if 'cost' in message_lower or 'price' in message_lower:
            base_suggestions.append("View pricing breakdown")
        if 'agent' in message_lower:
            base_suggestions.append("Browse AI agent catalog")
        if 'help' in message_lower or 'how' in message_lower:
            base_suggestions.append("View help documentation")
            
        return base_suggestions[:3]  # Max 3 suggestions
    
    def _generate_actions(self, context: Dict[str, Any], response: str) -> List[Dict[str, str]]:
        """Generate actionable buttons/links based on context and response"""
        
        platform_context = context.get('platform_context', {})
        primary_actions = platform_context.get('primary_actions', [])
        
        actions = []
        
        # Convert primary actions to UI actions
        action_map = {
            'explore_features': {"text": "Explore Features", "action": "/features"},
            'start_onboarding': {"text": "Start Tour", "action": "start_onboarding"},
            'view_analytics': {"text": "View Analytics", "action": "/dashboard/analytics"},
            'manage_agents': {"text": "Manage Agents", "action": "/agents"},
            'browse_agents': {"text": "Browse Agents", "action": "/agents/browse"},
            'install_agent': {"text": "Install Agent", "action": "show_agent_modal"},
            'update_profile': {"text": "Update Profile", "action": "/profile/edit"},
            'configure_preferences': {"text": "Settings", "action": "/profile/settings"}
        }
        
        for action_key in primary_actions[:2]:  # Max 2 actions
            if action_key in action_map:
                actions.append(action_map[action_key])
        
        return actions
    
    def _generate_fallback_response(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback response when OpenAI is unavailable"""
        
        # Simple keyword-based responses
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['help', 'start', 'how']):
            response = "I'm here to help you navigate CapeControl! Let me guide you through the platform features."
        elif any(word in message_lower for word in ['agent', 'ai']):
            response = "CapeControl offers a variety of AI agents for automation. Would you like to explore the agent marketplace?"
        elif any(word in message_lower for word in ['dashboard', 'analytics']):
            response = "Your dashboard shows key metrics and agent performance. I can help you interpret the data and optimize your setup."
        elif any(word in message_lower for word in ['cost', 'price', 'billing']):
            response = "I can help you understand CapeControl's pricing and optimize your costs. Would you like to review your usage?"
        else:
            response = "I understand you're asking about: " + message + ". Let me help you find the right information or feature."
        
        return {
            "response": response,
            "suggestions": self._generate_suggestions(context, message),
            "actions": self._generate_actions(context, response),
            "context": context
        }

# Initialize the service
cape_ai_service = CapeAIService()

@router.post("/prompt", response_model=AIResponse)
async def ai_prompt(
    request: AIPromptRequest,
    current_user: User = Depends(get_current_user)
):
    """Process AI conversation with intelligent context awareness"""
    
    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Analyze user context
    user_context = await cape_ai_service.analyze_user_context(current_user, request.context)
    
    # Get conversation history
    conversation_history = await cape_ai_service.get_conversation_history(session_id)
    
    # Save user message
    user_message = {
        "type": "user",
        "content": request.message,
        "timestamp": datetime.now().isoformat(),
        "context": user_context
    }
    await cape_ai_service.save_conversation(session_id, user_message)
    
    # Generate AI response
    ai_result = await cape_ai_service.generate_contextual_response(
        request.message, 
        user_context, 
        conversation_history
    )
    
    # Save AI response
    ai_message = {
        "type": "assistant", 
        "content": ai_result["response"],
        "timestamp": datetime.now().isoformat(),
        "suggestions": ai_result["suggestions"],
        "actions": ai_result["actions"]
    }
    await cape_ai_service.save_conversation(session_id, ai_message)
    
    return AIResponse(
        response=ai_result["response"],
        session_id=session_id,
        context=ai_result["context"],
        suggestions=ai_result["suggestions"],
        actions=ai_result["actions"]
    )

@router.get("/conversation/{session_id}")
async def get_conversation(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Retrieve conversation history"""
    
    history = await cape_ai_service.get_conversation_history(session_id)
    return {"session_id": session_id, "messages": history}

@router.delete("/conversation/{session_id}")
async def clear_conversation(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Clear conversation history"""
    
    try:
        history_key = f"cape_ai:conversation:{session_id}"
        redis_client.delete(history_key)
        return {"message": "Conversation cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation: {e}")

@router.get("/suggestions")
async def get_contextual_suggestions(
    current_path: str = "/",
    current_user: User = Depends(get_current_user)
):
    """Get contextual suggestions for current page"""
    
    context = {"currentPath": current_path}
    user_context = await cape_ai_service.analyze_user_context(current_user, context)
    suggestions = cape_ai_service._generate_suggestions(user_context, "")
    actions = cape_ai_service._generate_actions(user_context, "")
    
    return {
        "suggestions": suggestions,
        "actions": actions,
        "context": user_context
    }
