# CapeAI Backend Service Implementation - Multi-Provider Enhanced (Task 2.1.1)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
import redis
import json
import uuid
from datetime import datetime
import asyncio
import logging

from app.dependencies import get_current_user
# Import User directly from models.py to avoid circular import issues
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models import User
from typing import Any

# Type alias for User model
UserType = Any
from app.config import settings
from app.utils.input_sanitization import validate_ai_prompt, sanitize_text
from app.utils.content_moderation import moderate_ai_response, ModerationLevel
from app.services.ai_performance_service import get_ai_performance_monitor, AIProvider
from app.services.multi_provider_ai_service import (
    get_multi_provider_ai_service,
    ModelProvider,
    AIProviderResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["CapeAI"])

# Redis connection for conversation memory
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

class AIPromptRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None
    model: Optional[str] = None  # NEW: Allow model selection
    provider: Optional[str] = None  # NEW: Allow provider selection
    temperature: Optional[float] = None  # NEW: Allow temperature override
    max_tokens: Optional[int] = None  # NEW: Allow token limit override
    
    @validator('message')
    def validate_message(cls, v):
        """Validate and sanitize AI prompt message"""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        
        # Basic sanitization and validation
        result = sanitize_text(v, level="ai_prompt", field_type="ai_prompt")
        
        if not result["is_safe"]:
            # Log the threat but don't necessarily block
            logger.warning(f"AI prompt validation warnings: {result['threats_detected']}")
            
        # Return sanitized version
        return result["sanitized"]
    
    @validator('context')
    def validate_context(cls, v):
        """Validate context data for security"""
        if not v:
            return v
            
        # Sanitize context values that are strings
        sanitized_context = {}
        for key, value in v.items():
            if isinstance(value, str):
                result = sanitize_text(value, level="basic", field_type="general_text")
                sanitized_context[key] = result["sanitized"]
                if not result["is_safe"]:
                    logger.warning(f"Context field '{key}' sanitized: {result['threats_detected']}")
            else:
                sanitized_context[key] = value
                
        return sanitized_context
    
    @validator('provider')
    def validate_provider(cls, v):
        """Validate provider selection"""
        if v and v not in ['openai', 'claude']:
            raise ValueError(f"Invalid provider '{v}'. Must be 'openai' or 'claude'")
        return v
    
    @validator('temperature')
    def validate_temperature(cls, v):
        """Validate temperature parameter"""
        if v is not None and (v < 0 or v > 2):
            raise ValueError("Temperature must be between 0 and 2")
        return v
    
    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        """Validate max_tokens parameter"""
        if v is not None and (v < 1 or v > 8192):
            raise ValueError("max_tokens must be between 1 and 8192")
        return v

class AIResponse(BaseModel):
    response: str
    session_id: str
    context: Dict[str, Any]
    suggestions: List[str] = []
    actions: List[Dict[str, str]] = []
    content_warnings: List[str] = []
    moderation_applied: bool = False
    model_used: Optional[str] = None  # NEW: Track which model was used
    provider_used: Optional[str] = None  # NEW: Track which provider was used
    response_time_ms: Optional[int] = None  # NEW: Track response time

class CapeAIService:
    """Enhanced CapeAI service with multi-provider AI support (Task 2.1.1)"""
    
    def __init__(self):
        self.conversation_cache = {}
        self.user_profiles = {}
        self.multi_ai = get_multi_provider_ai_service()
        
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
    
    def select_optimal_model(
        self, 
        message: str, 
        user_context: Dict[str, Any],
        user_preference: Optional[str] = None,
        provider_preference: Optional[str] = None
    ) -> str:
        """Intelligently select the best model based on context and preferences"""
        
        # Respect user's explicit choices first
        if user_preference:
            config = self.multi_ai.get_model_config(user_preference)
            if config:
                return user_preference
        
        # Get available models
        available_models = self.multi_ai.get_available_models()
        
        # Provider preference handling
        if provider_preference and provider_preference in available_models:
            provider_models = available_models[provider_preference]
            if provider_models:
                # Default model for the provider
                return self.multi_ai.get_default_model(ModelProvider(provider_preference))
        
        # Context-based intelligent selection
        message_lower = message.lower()
        expertise_level = user_context.get('expertise_level', 'beginner')
        current_area = user_context.get('platform_context', {}).get('area', 'general')
        
        # For complex technical queries, prefer Claude (better reasoning)
        if any(keyword in message_lower for keyword in [
            'code', 'programming', 'debug', 'algorithm', 'technical', 'integration',
            'architecture', 'development', 'api', 'database', 'optimize'
        ]):
            if 'claude' in available_models and available_models['claude']:
                return 'claude-3-sonnet'  # Good balance of capability and cost
        
        # For creative or conversational queries, prefer GPT-4
        if any(keyword in message_lower for keyword in [
            'creative', 'write', 'story', 'marketing', 'content', 'social',
            'brainstorm', 'idea', 'strategy', 'plan'
        ]):
            if 'openai' in available_models and available_models['openai']:
                return 'gpt-4'
        
        # For quick, simple questions, prefer faster/cheaper models
        if len(message) < 100 and expertise_level == 'beginner':
            if 'claude' in available_models and 'claude-3-haiku' in available_models['claude']:
                return 'claude-3-haiku'  # Fast and cheap
            elif 'openai' in available_models and 'gpt-3.5-turbo' in available_models['openai']:
                return 'gpt-3.5-turbo'
        
        # For advanced users or complex queries, prefer high-capability models
        if expertise_level == 'advanced' or len(message) > 500:
            if 'claude' in available_models and 'claude-3-opus' in available_models['claude']:
                return 'claude-3-opus'  # Most capable
            elif 'openai' in available_models and 'gpt-4-turbo' in available_models['openai']:
                return 'gpt-4-turbo'
        
        # Default fallback
        return self.multi_ai.get_default_model()
    
    async def analyze_user_context(self, user: UserType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user context for personalized responses"""
        
        # Current page context
        current_page = context.get('currentPath', '/')
        onboarding_step = context.get('onboardingStep', 0)
        user_role = getattr(user, 'role', 'user')
        
        # Determine user expertise level
        account_age_days = (datetime.now() - user.created_at).days if hasattr(user, 'created_at') else 0
        expertise_level = 'beginner' if account_age_days < 7 else 'intermediate' if account_age_days < 30 else 'advanced'
        
        return {
            'user_id': str(user.id),  # Add user ID for performance monitoring
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
        conversation_history: List[Dict],
        model: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate AI response using multi-provider service with intelligent model selection"""
        
        # Select optimal model if not specified
        if not model:
            model = self.select_optimal_model(
                message, 
                user_context, 
                user_preference=model,
                provider_preference=provider
            )
        
        # Build context-aware system prompt
        system_prompt = self._build_system_prompt(user_context, model)
        
        # Prepare conversation messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        try:
            # Use multi-provider service for AI generation
            ai_response: AIProviderResponse = await self.multi_ai.generate_response(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                user_id=user_context.get('user_id')
            )
            
            # Generate contextual suggestions and actions
            suggestions = self._generate_suggestions(user_context, message)
            actions = self._generate_actions(user_context, ai_response.content)
            
            return {
                "response": ai_response.content,
                "suggestions": suggestions,
                "actions": actions,
                "context": user_context,
                "model_used": ai_response.model,
                "provider_used": ai_response.provider.value,
                "response_time_ms": ai_response.response_time_ms,
                "usage": ai_response.usage
            }
            
        except Exception as e:
            logger.error(f"Multi-provider AI error: {e}")
            # Fallback response
            fallback = self._generate_fallback_response(message, user_context)
            fallback.update({
                "model_used": "fallback",
                "provider_used": "local",
                "response_time_ms": 0,
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            })
            return fallback
    
    def _build_system_prompt(self, context: Dict[str, Any], model: str = "gpt-4") -> str:
        """Build context-aware system prompt with model-specific optimizations"""
        
        # Get model configuration for provider-specific optimizations
        model_config = self.multi_ai.get_model_config(model)
        provider = model_config.provider if model_config else ModelProvider.OPENAI
        
        base_prompt = """You are CapeAI, an intelligent assistant for the CapeControl platform - a professional AI-agents marketplace and automation platform.

Your personality: Helpful, professional, concise, and encouraging. You understand both technical and business aspects of AI automation.

Your role: Guide users through the platform, provide intelligent suggestions, help with onboarding, and assist with AI agent selection and management."""

        # Provider-specific optimizations
        if provider == ModelProvider.CLAUDE:
            base_prompt += "\n\nNote: You are powered by Claude, providing thoughtful analysis and clear reasoning for technical and strategic questions."
        elif provider == ModelProvider.OPENAI:
            base_prompt += "\n\nNote: You are powered by OpenAI, offering creative solutions and conversational assistance."

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
    current_user: UserType = Depends(get_current_user)
):
    """Process AI conversation with intelligent context awareness and enhanced security"""
    
    # Additional AI prompt validation beyond Pydantic validation
    ai_validation = validate_ai_prompt(request.message, request.context)
    
    # Log validation results
    if ai_validation["threats_detected"]:
        logger.info(f"AI prompt validation for user {current_user.id}: {ai_validation['threats_detected']}")
    
    # Check safety score - block extremely dangerous prompts
    if ai_validation["safety_score"] < 20:  # Very low safety score
        logger.warning(f"Blocking dangerous AI prompt from user {current_user.id}: safety_score={ai_validation['safety_score']}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Input validation failed",
                "message": "The prompt contains content that cannot be processed safely",
                "safety_score": ai_validation["safety_score"],
                "validation_id": ai_validation.get("validation_timestamp", "unknown")
            }
        )
    
    # Use the sanitized message for processing
    sanitized_message = ai_validation["sanitized"]
    
    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Analyze user context (using sanitized context from validation)
    sanitized_context = {k: v for k, v in request.context.items() if isinstance(v, (str, int, float, bool))}
    user_context = await cape_ai_service.analyze_user_context(current_user, sanitized_context)
    
    # Get conversation history
    conversation_history = await cape_ai_service.get_conversation_history(session_id)
    
    # Save user message (with original message for context, but mark sanitization)
    user_message = {
        "type": "user",
        "content": sanitized_message,
        "original_length": len(request.message),
        "sanitized": len(ai_validation["threats_detected"]) > 0,
        "timestamp": datetime.now().isoformat(),
        "context": user_context,
        "safety_score": ai_validation["safety_score"]
    }
    await cape_ai_service.save_conversation(session_id, user_message)
    
    # Generate AI response using enhanced multi-provider service
    ai_result = await cape_ai_service.generate_contextual_response(
        sanitized_message,  # Use sanitized version
        user_context, 
        conversation_history,
        model=request.model,
        provider=request.provider,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    # Apply comprehensive content moderation to AI response
    user_context_for_moderation = {
        "user_id": current_user.id,
        "endpoint": "/api/ai/prompt",
        "session_id": session_id,
        "user_expertise": user_context.get("expertise_level", "beginner")
    }
    
    moderation_result = moderate_ai_response(
        ai_result["response"],
        user_context_for_moderation,
        ModerationLevel.STANDARD
    )
    
    # Handle blocked content
    if not moderation_result.is_safe and moderation_result.suggested_action == "block":
        logger.warning(
            f"AI response blocked for user {current_user.id}: "
            f"violations={[v.value for v in moderation_result.violations]}"
        )
        
        # Return safe fallback response
        fallback_response = "I apologize, but I cannot provide that response due to content policy restrictions. Please try rephrasing your question or ask about something else I can help with."
        
        moderated_content = fallback_response
        content_warnings = ["Content moderation applied"]
    else:
        moderated_content = moderation_result.moderated_content
        content_warnings = []
        if moderation_result.violations:
            content_warnings.append(f"Content reviewed: {moderation_result.explanation}")
    
    # Log moderation results for monitoring
    if moderation_result.violations:
        logger.info(
            f"AI response moderation for user {current_user.id}: "
            f"category={moderation_result.category.value}, "
            f"violations={[v.value for v in moderation_result.violations]}, "
            f"confidence={moderation_result.confidence_score:.1f}%"
        )
    
    # Save AI response with moderation metadata
    ai_message = {
        "type": "assistant", 
        "content": moderated_content,
        "timestamp": datetime.now().isoformat(),
        "suggestions": ai_result["suggestions"],
        "actions": ai_result["actions"],
        "input_sanitized": len(ai_validation["threats_detected"]) > 0,
        "content_moderated": len(moderation_result.violations) > 0,
        "moderation_category": moderation_result.category.value,
        "content_warnings": content_warnings
    }
    await cape_ai_service.save_conversation(session_id, ai_message)
    
    return AIResponse(
        response=moderated_content,
        session_id=session_id,
        context=ai_result["context"],
        suggestions=ai_result["suggestions"],
        actions=ai_result["actions"],
        content_warnings=content_warnings,
        moderation_applied=len(moderation_result.violations) > 0,
        model_used=ai_result.get("model_used"),
        provider_used=ai_result.get("provider_used"),
        response_time_ms=ai_result.get("response_time_ms")
    )

@router.get("/conversation/{session_id}")
async def get_conversation(
    session_id: str,
    current_user: UserType = Depends(get_current_user)
):
    """Retrieve conversation history"""
    
    history = await cape_ai_service.get_conversation_history(session_id)
    return {"session_id": session_id, "messages": history}

@router.delete("/conversation/{session_id}")
async def clear_conversation(
    session_id: str,
    current_user: UserType = Depends(get_current_user)
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
    current_user: UserType = Depends(get_current_user)
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

@router.get("/models")
async def get_available_models(current_user: UserType = Depends(get_current_user)):
    """Get all available AI models and providers"""
    
    multi_ai = get_multi_provider_ai_service()
    
    return {
        "available_models": multi_ai.get_available_models(),
        "provider_status": await multi_ai.get_provider_status(),
        "default_model": multi_ai.get_default_model()
    }

@router.get("/models/{model_name}")
async def get_model_info(
    model_name: str,
    current_user: UserType = Depends(get_current_user)
):
    """Get detailed information about a specific model"""
    
    multi_ai = get_multi_provider_ai_service()
    config = multi_ai.get_model_config(model_name)
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
    
    return {
        "model_name": model_name,
        "provider": config.provider.value,
        "config": {
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "supports_streaming": config.supports_streaming,
            "context_window": config.context_window,
            "cost_per_1k_prompt": config.cost_per_1k_prompt,
            "cost_per_1k_completion": config.cost_per_1k_completion
        }
    }

@router.post("/models/recommend")
async def recommend_model(
    request: dict,
    current_user: UserType = Depends(get_current_user)
):
    """Get model recommendation based on query and context"""
    
    message = request.get("message", "")
    context = request.get("context", {})
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required for recommendation")
    
    user_context = await cape_ai_service.analyze_user_context(current_user, context)
    recommended_model = cape_ai_service.select_optimal_model(message, user_context)
    
    multi_ai = get_multi_provider_ai_service()
    model_config = multi_ai.get_model_config(recommended_model)
    
    return {
        "recommended_model": recommended_model,
        "provider": model_config.provider.value if model_config else "unknown",
        "reasoning": _get_recommendation_reasoning(message, user_context, recommended_model),
        "alternatives": _get_alternative_models(recommended_model, multi_ai)
    }

def _get_recommendation_reasoning(message: str, context: Dict[str, Any], model: str) -> str:
    """Generate reasoning for model recommendation"""
    
    message_lower = message.lower()
    expertise = context.get('expertise_level', 'beginner')
    
    if 'claude' in model:
        if any(keyword in message_lower for keyword in ['code', 'technical', 'debug']):
            return "Claude excels at technical reasoning and code analysis tasks"
        elif expertise == 'advanced':
            return "Claude provides sophisticated analysis suitable for advanced users"
        elif 'haiku' in model:
            return "Claude Haiku offers fast responses for quick questions"
        else:
            return "Claude Sonnet provides excellent balance of capability and efficiency"
    
    elif 'gpt' in model:
        if any(keyword in message_lower for keyword in ['creative', 'write', 'marketing']):
            return "GPT-4 excels at creative and conversational tasks"
        elif 'turbo' in model:
            return "GPT-4 Turbo offers enhanced capabilities for complex queries"
        else:
            return "GPT-4 provides reliable general-purpose assistance"
    
    return "Selected based on query complexity and user context"

def _get_alternative_models(recommended: str, multi_ai) -> List[Dict[str, str]]:
    """Get alternative model suggestions"""
    
    available = multi_ai.get_available_models()
    alternatives = []
    
    # Get configs for comparison
    recommended_config = multi_ai.get_model_config(recommended)
    
    for provider, models in available.items():
        for model in models[:2]:  # Limit alternatives
            if model != recommended:
                config = multi_ai.get_model_config(model)
                if config:
                    alternatives.append({
                        "model": model,
                        "provider": provider,
                        "reason": f"Alternative {provider} option" + 
                                (f" - lower cost" if config.cost_per_1k_prompt < recommended_config.cost_per_1k_prompt else "")
                    })
    
    return alternatives[:3]  # Max 3 alternatives
