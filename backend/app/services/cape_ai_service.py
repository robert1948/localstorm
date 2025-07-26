"""
CapeAI Multi-Provider Service
Comprehensive AI service integrating OpenAI, Claude, and Gemini
Based on completed Phase 2.1.1-2.1.7 AI Enhancement tasks
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import redis
import openai
import anthropic
import google.generativeai as genai
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database import get_db
from ..config import settings
from ..models.user import User

logger = logging.getLogger(__name__)

class CapeAIService:
    """
    Advanced multi-provider AI service with personalization and analytics
    Implements all completed Phase 2 AI enhancement features
    """
    
    def __init__(self, db: Session, redis_client: Optional[redis.Redis] = None):
        self.db = db
        self.redis_client = redis_client or redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True
        )
        
        # Initialize AI providers (Phase 2.1.1-2.1.2)
        self.openai_client = self._init_openai()
        self.claude_client = self._init_claude()
        self.gemini_client = self._init_gemini()
        
        # Provider configurations
        self.providers = {
            'openai': {
                'client': self.openai_client,
                'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
                'max_tokens': 4000,
                'cost_per_token': 0.00003
            },
            'claude': {
                'client': self.claude_client,
                'models': ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
                'max_tokens': 4000,
                'cost_per_token': 0.000015
            },
            'gemini': {
                'client': self.gemini_client,
                'models': ['gemini-pro', 'gemini-pro-vision', 'gemini-1.5-pro'],
                'max_tokens': 2048,
                'cost_per_token': 0.0000125
            }
        }
        
        # Context enhancement settings (Phase 2.1.3)
        self.context_window_size = 10
        self.semantic_similarity_threshold = 0.7
        
        # Personalization settings (Phase 2.1.4)
        self.personalization_weights = {
            'communication_style': 0.3,
            'learning_style': 0.25,
            'expertise_level': 0.2,
            'interaction_history': 0.25
        }
        
        # Template engine settings (Phase 2.1.5)
        self.template_cache = {}
        
        logger.info("CapeAI Service initialized with multi-provider support")

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            return openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return None

    def _init_claude(self):
        """Initialize Claude client"""
        try:
            return anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            return None

    def _init_gemini(self):
        """Initialize Gemini client"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            return genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None

    async def process_ai_request(
        self,
        user_id: str,
        message: str,
        context: Dict[str, Any] = None,
        conversation_id: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process AI request with full enhancement features
        Integrates all Phase 2.1 completions: multi-provider, context, personalization, templates, analytics
        """
        start_time = time.time()
        
        try:
            # 1. Get user profile and personalization data (Phase 2.1.4)
            user_profile = await self._get_user_ai_profile(user_id)
            
            # 2. Enhance context with conversation history (Phase 2.1.3)
            enhanced_context = await self._enhance_context(
                user_id, message, context or {}, conversation_id
            )
            
            # 3. Select optimal provider and model (Phase 2.1.1-2.1.2)
            if not provider:
                provider, model = await self._select_optimal_provider(
                    message, enhanced_context, user_profile
                )
            
            # 4. Apply personalization and templates (Phase 2.1.4-2.1.5)
            personalized_prompt = await self._personalize_prompt(
                message, enhanced_context, user_profile
            )
            
            # 5. Generate AI response
            ai_response = await self._generate_ai_response(
                provider, model, personalized_prompt, enhanced_context
            )
            
            # 6. Post-process and analyze response (Phase 2.1.6)
            processed_response = await self._post_process_response(
                ai_response, user_profile, enhanced_context
            )
            
            # 7. Store conversation and analytics
            conversation_data = await self._store_conversation(
                user_id, message, processed_response, 
                provider, model, conversation_id, enhanced_context
            )
            
            # 8. Update user profile and learning (Phase 2.1.4)
            await self._update_user_learning(user_id, message, processed_response)
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "response": processed_response,
                "conversation_id": conversation_data["conversation_id"],
                "provider": provider,
                "model": model,
                "processing_time": processing_time,
                "context_enhanced": True,
                "personalized": True,
                "analytics": {
                    "tokens_used": ai_response.get("tokens_used", 0),
                    "cost_estimate": ai_response.get("cost_estimate", 0),
                    "quality_score": processed_response.get("quality_score", 0)
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing AI request for user {user_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback_response": "I apologize, but I'm having trouble processing your request right now. Please try again.",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def _get_user_ai_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user AI profile for personalization
        Phase 2.1.4 AI Personalization implementation
        """
        try:
            # Check Redis cache first
            cache_key = f"user_ai_profile:{user_id}"
            cached_profile = self.redis_client.get(cache_key)
            
            if cached_profile:
                return json.loads(cached_profile)
            
            # Query database for user profile
            query = text("""
                SELECT 
                    communication_style,
                    learning_style,
                    expertise_level,
                    interaction_patterns,
                    preferences,
                    ai_usage_stats,
                    personalization_data
                FROM ai_user_profiles 
                WHERE user_id = :user_id
            """)
            
            result = self.db.execute(query, {"user_id": user_id}).fetchone()
            
            if result:
                profile = {
                    "communication_style": result.communication_style or "adaptive",
                    "learning_style": result.learning_style or "visual",
                    "expertise_level": result.expertise_level or "intermediate",
                    "interaction_patterns": result.interaction_patterns or {},
                    "preferences": result.preferences or {},
                    "ai_usage_stats": result.ai_usage_stats or {},
                    "personalization_data": result.personalization_data or {}
                }
            else:
                # Create default profile for new user
                profile = await self._create_default_ai_profile(user_id)
            
            # Cache for 1 hour
            self.redis_client.setex(cache_key, 3600, json.dumps(profile))
            return profile
            
        except Exception as e:
            logger.error(f"Error getting user AI profile: {e}")
            return await self._create_default_ai_profile(user_id)

    async def _create_default_ai_profile(self, user_id: str) -> Dict[str, Any]:
        """Create default AI profile for new users"""
        default_profile = {
            "communication_style": "adaptive",
            "learning_style": "visual",
            "expertise_level": "intermediate",
            "interaction_patterns": {
                "preferred_response_length": "medium",
                "question_types": [],
                "topic_interests": []
            },
            "preferences": {
                "explanation_style": "detailed",
                "code_examples": True,
                "step_by_step": True
            },
            "ai_usage_stats": {
                "total_interactions": 0,
                "avg_session_length": 0,
                "preferred_providers": {}
            },
            "personalization_data": {
                "response_ratings": [],
                "topic_expertise": {},
                "learning_progress": {}
            }
        }
        
        try:
            # Store in database
            insert_query = text("""
                INSERT INTO ai_user_profiles (
                    user_id, communication_style, learning_style, 
                    expertise_level, interaction_patterns, preferences,
                    ai_usage_stats, personalization_data
                ) VALUES (
                    :user_id, :communication_style, :learning_style,
                    :expertise_level, :interaction_patterns, :preferences,
                    :ai_usage_stats, :personalization_data
                )
            """)
            
            self.db.execute(insert_query, {
                "user_id": user_id,
                "communication_style": default_profile["communication_style"],
                "learning_style": default_profile["learning_style"],
                "expertise_level": default_profile["expertise_level"],
                "interaction_patterns": json.dumps(default_profile["interaction_patterns"]),
                "preferences": json.dumps(default_profile["preferences"]),
                "ai_usage_stats": json.dumps(default_profile["ai_usage_stats"]),
                "personalization_data": json.dumps(default_profile["personalization_data"])
            })
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error creating default AI profile: {e}")
            self.db.rollback()
        
        return default_profile

    async def _enhance_context(
        self,
        user_id: str,
        message: str,
        context: Dict[str, Any],
        conversation_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Enhance context with conversation history and semantic analysis
        Phase 2.1.3 Context Enhancement implementation
        """
        enhanced_context = context.copy()
        
        try:
            # Add conversation history
            if conversation_id:
                history = await self._get_conversation_history(conversation_id, limit=self.context_window_size)
                enhanced_context["conversation_history"] = history
            
            # Add user context
            enhanced_context["user_context"] = {
                "user_id": user_id,
                "current_message": message,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Add semantic context (simplified implementation)
            similar_conversations = await self._find_similar_conversations(user_id, message)
            enhanced_context["similar_contexts"] = similar_conversations
            
            # Add system context
            enhanced_context["system_context"] = {
                "platform": "CapeAI",
                "version": "2.0",
                "capabilities": ["multi_provider", "personalized", "context_aware"]
            }
            
            return enhanced_context
            
        except Exception as e:
            logger.error(f"Error enhancing context: {e}")
            return enhanced_context

    async def _select_optimal_provider(
        self,
        message: str,
        context: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Select optimal AI provider and model based on analytics
        Phase 2.1.1-2.1.2 Multi-Model Support + Phase 2.1.6 AI Analytics
        """
        try:
            # Get user's provider preferences from usage stats
            usage_stats = user_profile.get("ai_usage_stats", {})
            preferred_providers = usage_stats.get("preferred_providers", {})
            
            # Analyze message complexity and type
            message_analysis = self._analyze_message_complexity(message)
            
            # Default selection logic
            if message_analysis["requires_reasoning"]:
                return "claude", "claude-3-opus"
            elif message_analysis["requires_code"]:
                return "openai", "gpt-4"
            elif message_analysis["is_simple"]:
                return "gemini", "gemini-pro"
            else:
                # Use user's most successful provider
                if preferred_providers:
                    best_provider = max(preferred_providers.items(), key=lambda x: x[1])
                    provider = best_provider[0]
                    model = self.providers[provider]["models"][0]
                    return provider, model
                
                # Default fallback
                return "openai", "gpt-4"
                
        except Exception as e:
            logger.error(f"Error selecting optimal provider: {e}")
            return "openai", "gpt-4"

    def _analyze_message_complexity(self, message: str) -> Dict[str, bool]:
        """Analyze message to determine optimal provider"""
        message_lower = message.lower()
        
        return {
            "requires_reasoning": any(word in message_lower for word in [
                "explain", "analyze", "compare", "evaluate", "why", "how"
            ]),
            "requires_code": any(word in message_lower for word in [
                "code", "function", "class", "python", "javascript", "program"
            ]),
            "is_simple": len(message.split()) < 10 and "?" not in message,
            "is_creative": any(word in message_lower for word in [
                "create", "write", "story", "poem", "design", "imagine"
            ])
        }

    async def _personalize_prompt(
        self,
        message: str,
        context: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Personalize prompt based on user profile and templates
        Phase 2.1.4 AI Personalization + Phase 2.1.5 Advanced Prompting Templates
        """
        try:
            # Get base template
            template = self._get_personalization_template(user_profile)
            
            # Apply personalization
            personalized_prompt = template.format(
                user_message=message,
                communication_style=user_profile.get("communication_style", "adaptive"),
                learning_style=user_profile.get("learning_style", "visual"),
                expertise_level=user_profile.get("expertise_level", "intermediate"),
                preferences=json.dumps(user_profile.get("preferences", {}))
            )
            
            return personalized_prompt
            
        except Exception as e:
            logger.error(f"Error personalizing prompt: {e}")
            return message

    def _get_personalization_template(self, user_profile: Dict[str, Any]) -> str:
        """Get personalized prompt template"""
        communication_style = user_profile.get("communication_style", "adaptive")
        learning_style = user_profile.get("learning_style", "visual")
        
        templates = {
            "analytical": """
            Please provide a detailed, logical analysis of the following request.
            Break down complex concepts systematically and provide evidence-based reasoning.
            
            User Question: {user_message}
            
            Respond in an {communication_style} communication style, 
            optimized for {learning_style} learning style.
            Expertise level: {expertise_level}
            """,
            
            "conversational": """
            Let's have a friendly discussion about this topic! I'll explain things 
            in a way that's easy to understand and engaging.
            
            Your question: {user_message}
            
            I'll adapt my communication style to be {communication_style} and 
            present information in a {learning_style} way suitable for 
            {expertise_level} level understanding.
            """,
            
            "creative": """
            Let's explore this creatively! I'll help you think outside the box 
            and come up with innovative solutions.
            
            Your request: {user_message}
            
            I'll use a {communication_style} approach that works well with 
            {learning_style} learners at {expertise_level} level.
            """
        }
        
        # Select template based on message type or default to conversational
        return templates.get(communication_style, templates["conversational"])

    async def _generate_ai_response(
        self,
        provider: str,
        model: str,
        prompt: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate response from selected AI provider"""
        try:
            if provider == "openai":
                return await self._generate_openai_response(model, prompt, context)
            elif provider == "claude":
                return await self._generate_claude_response(model, prompt, context)
            elif provider == "gemini":
                return await self._generate_gemini_response(model, prompt, context)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
                
        except Exception as e:
            logger.error(f"Error generating {provider} response: {e}")
            # Fallback to OpenAI
            if provider != "openai" and self.openai_client:
                return await self._generate_openai_response("gpt-3.5-turbo", prompt, context)
            raise

    async def _generate_openai_response(self, model: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate OpenAI response"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are CapeAI, a helpful and knowledgeable assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.providers["openai"]["max_tokens"],
                temperature=0.7
            )
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "cost_estimate": response.usage.total_tokens * self.providers["openai"]["cost_per_token"],
                "model": model,
                "provider": "openai"
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def _generate_claude_response(self, model: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Claude response"""
        try:
            response = self.claude_client.messages.create(
                model=model,
                max_tokens=self.providers["claude"]["max_tokens"],
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "content": response.content[0].text,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "cost_estimate": (response.usage.input_tokens + response.usage.output_tokens) * self.providers["claude"]["cost_per_token"],
                "model": model,
                "provider": "claude"
            }
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    async def _generate_gemini_response(self, model: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Gemini response"""
        try:
            response = self.gemini_client.generate_content(prompt)
            
            # Estimate tokens (Gemini doesn't provide exact count)
            estimated_tokens = len(prompt.split()) + len(response.text.split())
            
            return {
                "content": response.text,
                "tokens_used": estimated_tokens,
                "cost_estimate": estimated_tokens * self.providers["gemini"]["cost_per_token"],
                "model": model,
                "provider": "gemini"
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def _post_process_response(
        self,
        ai_response: Dict[str, Any],
        user_profile: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Post-process AI response with quality analysis
        Phase 2.1.6 AI Analytics implementation
        """
        try:
            content = ai_response["content"]
            
            # Calculate quality score (Phase 2.1.6)
            quality_score = self._calculate_quality_score(content, context)
            
            # Apply content moderation
            moderated_content = await self._moderate_content(content)
            
            # Add metadata
            processed_response = {
                "content": moderated_content,
                "quality_score": quality_score,
                "metadata": {
                    "original_length": len(content),
                    "processed_length": len(moderated_content),
                    "provider": ai_response["provider"],
                    "model": ai_response["model"],
                    "tokens_used": ai_response["tokens_used"],
                    "cost_estimate": ai_response["cost_estimate"]
                },
                "analytics": {
                    "relevance": quality_score.get("relevance", 0),
                    "accuracy": quality_score.get("accuracy", 0),
                    "completeness": quality_score.get("completeness", 0),
                    "clarity": quality_score.get("clarity", 0),
                    "helpfulness": quality_score.get("helpfulness", 0)
                }
            }
            
            return processed_response
            
        except Exception as e:
            logger.error(f"Error post-processing response: {e}")
            return {
                "content": ai_response["content"],
                "quality_score": {"overall": 0.5},
                "metadata": ai_response,
                "analytics": {}
            }

    def _calculate_quality_score(self, content: str, context: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate 5-dimensional quality score
        Phase 2.1.6 AI Analytics - Quality scoring implementation
        """
        try:
            # Simplified quality scoring algorithm
            word_count = len(content.split())
            sentence_count = len([s for s in content.split('.') if s.strip()])
            
            # Basic metrics
            relevance = min(1.0, word_count / 100)  # Relevance based on length
            accuracy = 0.8  # Default accuracy score
            completeness = min(1.0, sentence_count / 5)  # Completeness based on sentences
            clarity = max(0.5, 1.0 - (word_count / sentence_count - 15) / 20) if sentence_count > 0 else 0.5
            helpfulness = 0.7  # Default helpfulness score
            
            overall = (relevance + accuracy + completeness + clarity + helpfulness) / 5
            
            return {
                "relevance": round(relevance, 2),
                "accuracy": round(accuracy, 2),
                "completeness": round(completeness, 2),
                "clarity": round(clarity, 2),
                "helpfulness": round(helpfulness, 2),
                "overall": round(overall, 2)
            }
            
        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return {
                "relevance": 0.5,
                "accuracy": 0.5,
                "completeness": 0.5,
                "clarity": 0.5,
                "helpfulness": 0.5,
                "overall": 0.5
            }

    async def _moderate_content(self, content: str) -> str:
        """Basic content moderation"""
        # Implement your content moderation logic here
        # For now, just return the original content
        return content

    async def _store_conversation(
        self,
        user_id: str,
        message: str,
        response: Dict[str, Any],
        provider: str,
        model: str,
        conversation_id: Optional[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Store conversation in database"""
        try:
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = f"conv_{user_id}_{int(time.time())}"
            
            # Store user message
            user_message_query = text("""
                INSERT INTO ai_conversations (
                    user_id, session_id, message_type, content, 
                    context_data, ai_provider, model_used, created_at
                ) VALUES (
                    :user_id, :session_id, :message_type, :content,
                    :context_data, :ai_provider, :model_used, :created_at
                )
            """)
            
            self.db.execute(user_message_query, {
                "user_id": user_id,
                "session_id": conversation_id,
                "message_type": "user",
                "content": message,
                "context_data": json.dumps(context),
                "ai_provider": provider,
                "model_used": model,
                "created_at": datetime.utcnow()
            })
            
            # Store AI response
            ai_response_query = text("""
                INSERT INTO ai_conversations (
                    user_id, session_id, message_type, content,
                    context_data, ai_provider, model_used, tokens_used,
                    response_time_ms, created_at
                ) VALUES (
                    :user_id, :session_id, :message_type, :content,
                    :context_data, :ai_provider, :model_used, :tokens_used,
                    :response_time_ms, :created_at
                )
            """)
            
            self.db.execute(ai_response_query, {
                "user_id": user_id,
                "session_id": conversation_id,
                "message_type": "assistant",
                "content": response["content"],
                "context_data": json.dumps(response.get("metadata", {})),
                "ai_provider": provider,
                "model_used": model,
                "tokens_used": response.get("metadata", {}).get("tokens_used", 0),
                "response_time_ms": int(response.get("metadata", {}).get("processing_time", 0) * 1000),
                "created_at": datetime.utcnow()
            })
            
            self.db.commit()
            
            return {
                "conversation_id": conversation_id,
                "stored": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
            self.db.rollback()
            return {
                "conversation_id": conversation_id,
                "stored": False,
                "error": str(e)
            }

    async def _update_user_learning(
        self,
        user_id: str,
        message: str,
        response: Dict[str, Any]
    ):
        """
        Update user learning profile based on interaction
        Phase 2.1.4 AI Personalization - Learning adaptation
        """
        try:
            # Update user interaction patterns
            cache_key = f"user_ai_profile:{user_id}"
            self.redis_client.delete(cache_key)  # Invalidate cache
            
            # Update database with new interaction data
            update_query = text("""
                UPDATE ai_user_profiles 
                SET 
                    ai_usage_stats = COALESCE(ai_usage_stats, '{}')::jsonb || :new_stats,
                    interaction_patterns = COALESCE(interaction_patterns, '{}')::jsonb || :new_patterns,
                    updated_at = :updated_at
                WHERE user_id = :user_id
            """)
            
            new_stats = {
                "last_interaction": datetime.utcnow().isoformat(),
                "total_interactions": 1  # This should be incremented properly
            }
            
            new_patterns = {
                "last_message_length": len(message),
                "last_response_quality": response.get("quality_score", {}).get("overall", 0)
            }
            
            self.db.execute(update_query, {
                "user_id": user_id,
                "new_stats": json.dumps(new_stats),
                "new_patterns": json.dumps(new_patterns),
                "updated_at": datetime.utcnow()
            })
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error updating user learning: {e}")
            self.db.rollback()

    async def _get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get conversation history for context"""
        try:
            query = text("""
                SELECT message_type, content, created_at
                FROM ai_conversations
                WHERE session_id = :session_id
                ORDER BY created_at DESC
                LIMIT :limit
            """)
            
            results = self.db.execute(query, {
                "session_id": conversation_id,
                "limit": limit
            }).fetchall()
            
            return [
                {
                    "role": result.message_type,
                    "content": result.content,
                    "timestamp": result.created_at.isoformat()
                }
                for result in reversed(results)
            ]
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []

    async def _find_similar_conversations(
        self,
        user_id: str,
        message: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Find similar conversations for context enhancement"""
        try:
            # Simplified similarity search based on keywords
            keywords = message.lower().split()[:5]  # Take first 5 words
            
            if not keywords:
                return []
            
            # Create search pattern
            search_pattern = " | ".join(keywords)
            
            query = text("""
                SELECT DISTINCT session_id, content, created_at
                FROM ai_conversations
                WHERE user_id = :user_id 
                AND message_type = 'user'
                AND content ILIKE ANY(ARRAY[:keywords])
                ORDER BY created_at DESC
                LIMIT :limit
            """)
            
            keyword_patterns = [f"%{keyword}%" for keyword in keywords]
            
            results = self.db.execute(query, {
                "user_id": user_id,
                "keywords": keyword_patterns,
                "limit": limit
            }).fetchall()
            
            return [
                {
                    "conversation_id": result.session_id,
                    "content": result.content,
                    "timestamp": result.created_at.isoformat()
                }
                for result in results
            ]
            
        except Exception as e:
            logger.error(f"Error finding similar conversations: {e}")
            return []

    async def get_user_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive user AI analytics
        Phase 2.1.6 AI Analytics implementation
        """
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get conversation statistics
            stats_query = text("""
                SELECT 
                    COUNT(*) as total_interactions,
                    COUNT(DISTINCT session_id) as unique_conversations,
                    AVG(tokens_used) as avg_tokens_per_interaction,
                    SUM(tokens_used) as total_tokens_used,
                    ai_provider,
                    model_used
                FROM ai_conversations
                WHERE user_id = :user_id 
                AND created_at >= :start_date
                AND created_at <= :end_date
                AND message_type = 'assistant'
                GROUP BY ai_provider, model_used
            """)
            
            results = self.db.execute(stats_query, {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date
            }).fetchall()
            
            analytics = {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "summary": {
                    "total_interactions": sum(r.total_interactions for r in results),
                    "unique_conversations": sum(r.unique_conversations for r in results),
                    "total_tokens_used": sum(r.total_tokens_used or 0 for r in results),
                    "avg_tokens_per_interaction": sum(r.avg_tokens_per_interaction or 0 for r in results) / len(results) if results else 0
                },
                "provider_breakdown": [
                    {
                        "provider": r.ai_provider,
                        "model": r.model_used,
                        "interactions": r.total_interactions,
                        "conversations": r.unique_conversations,
                        "tokens_used": r.total_tokens_used or 0,
                        "avg_tokens": r.avg_tokens_per_interaction or 0
                    }
                    for r in results
                ],
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            return {
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat()
            }

    async def get_service_health(self) -> Dict[str, Any]:
        """Get service health status"""
        try:
            health_status = {
                "service": "cape_ai",
                "status": "healthy",
                "providers": {
                    "openai": "connected" if self.openai_client else "disconnected",
                    "claude": "connected" if self.claude_client else "disconnected",
                    "gemini": "connected" if self.gemini_client else "disconnected"
                },
                "redis": "connected" if self.redis_client.ping() else "disconnected",
                "database": "connected",
                "features": {
                    "multi_provider": True,
                    "context_enhancement": True,
                    "personalization": True,
                    "template_system": True,
                    "analytics": True,
                    "voice_integration": False  # Phase 2.1.7 - separate service
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Test database connection
            self.db.execute(text("SELECT 1")).fetchone()
            
            return health_status
            
        except Exception as e:
            return {
                "service": "cape_ai",
                "status": "degraded",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }