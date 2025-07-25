"""
Multi-Provider AI Service for Task 2.1.1: Claude Integration
============================================================

Enhanced AI service supporting multiple providers:
- OpenAI (existing)
- Claude (Anthropic) - NEW
- Unified interface for seamless provider switching
- Provider-specific optimizations and configurations
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Provider-specific imports
from openai import AsyncOpenAI
import anthropic
from pydantic import BaseModel

from app.config import settings
from app.services.ai_performance_service import get_ai_performance_monitor, AIProvider

logger = logging.getLogger(__name__)


class ModelProvider(str, Enum):
    """Available AI model providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    # GEMINI will be added in Task 2.1.2


@dataclass
class AIModelConfig:
    """Configuration for AI models"""
    provider: ModelProvider
    model_name: str
    max_tokens: int
    temperature: float
    supports_streaming: bool
    cost_per_1k_prompt: float
    cost_per_1k_completion: float
    context_window: int


@dataclass
class AIProviderResponse:
    """Standardized response from AI providers"""
    content: str
    provider: ModelProvider
    model: str
    usage: Dict[str, int]
    response_time_ms: int
    finish_reason: str
    metadata: Dict[str, Any] = None


class MultiProviderAIService:
    """Enhanced AI service with multi-provider support"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_monitor = get_ai_performance_monitor()
        
        # Initialize provider clients
        self.clients = {}
        self.model_configs = {}
        
        self._initialize_providers()
        self._setup_model_configurations()
    
    def _initialize_providers(self):
        """Initialize all available AI provider clients"""
        
        # OpenAI client (existing)
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            self.clients[ModelProvider.OPENAI] = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY
            )
            self.logger.info("OpenAI client initialized successfully")
        else:
            self.logger.warning("OpenAI API key not found - OpenAI models unavailable")
        
        # Claude (Anthropic) client - NEW
        claude_api_key = getattr(settings, 'CLAUDE_API_KEY', os.getenv('CLAUDE_API_KEY'))
        if claude_api_key:
            self.clients[ModelProvider.CLAUDE] = anthropic.AsyncAnthropic(
                api_key=claude_api_key
            )
            self.logger.info("Claude client initialized successfully")
        else:
            self.logger.warning("Claude API key not found - Claude models unavailable")
    
    def _setup_model_configurations(self):
        """Setup configurations for all supported models"""
        
        # OpenAI model configurations
        self.model_configs.update({
            "gpt-4": AIModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.03,
                cost_per_1k_completion=0.06,
                context_window=8192
            ),
            "gpt-4-turbo": AIModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-4-turbo",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.01,
                cost_per_1k_completion=0.03,
                context_window=128000
            ),
            "gpt-3.5-turbo": AIModelConfig(
                provider=ModelProvider.OPENAI,
                model_name="gpt-3.5-turbo",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.0015,
                cost_per_1k_completion=0.002,
                context_window=16385
            )
        })
        
        # Claude model configurations - NEW
        self.model_configs.update({
            "claude-3-opus": AIModelConfig(
                provider=ModelProvider.CLAUDE,
                model_name="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.015,
                cost_per_1k_completion=0.075,
                context_window=200000
            ),
            "claude-3-sonnet": AIModelConfig(
                provider=ModelProvider.CLAUDE,
                model_name="claude-3-sonnet-20240229",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.003,
                cost_per_1k_completion=0.015,
                context_window=200000
            ),
            "claude-3-haiku": AIModelConfig(
                provider=ModelProvider.CLAUDE,
                model_name="claude-3-haiku-20240307",
                max_tokens=4096,
                temperature=0.7,
                supports_streaming=True,
                cost_per_1k_prompt=0.00025,
                cost_per_1k_completion=0.00125,
                context_window=200000
            )
        })
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get all available models grouped by provider"""
        
        available = {}
        
        for model_key, config in self.model_configs.items():
            provider_name = config.provider.value
            if config.provider in self.clients:
                if provider_name not in available:
                    available[provider_name] = []
                available[provider_name].append(model_key)
        
        return available
    
    def get_model_config(self, model_name: str) -> Optional[AIModelConfig]:
        """Get configuration for a specific model"""
        return self.model_configs.get(model_name)
    
    def get_default_model(self, provider: Optional[ModelProvider] = None) -> str:
        """Get the default model for a provider or overall default"""
        
        # Provider-specific defaults
        if provider == ModelProvider.OPENAI:
            return "gpt-4"
        elif provider == ModelProvider.CLAUDE:
            return "claude-3-sonnet"
        
        # Overall default - prefer Claude Sonnet for better performance/cost ratio
        if ModelProvider.CLAUDE in self.clients:
            return "claude-3-sonnet"
        elif ModelProvider.OPENAI in self.clients:
            return "gpt-4"
        
        # Fallback
        available_models = list(self.model_configs.keys())
        return available_models[0] if available_models else "gpt-3.5-turbo"
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        user_id: Optional[str] = None,
        **kwargs
    ) -> AIProviderResponse:
        """Generate AI response using specified or default model"""
        
        # Use default model if none specified
        if not model:
            model = self.get_default_model()
        
        # Get model configuration
        config = self.get_model_config(model)
        if not config:
            raise ValueError(f"Model '{model}' not found or not configured")
        
        # Check if provider client is available
        if config.provider not in self.clients:
            raise ValueError(f"Provider '{config.provider.value}' not available")
        
        # Use config defaults if parameters not specified
        temperature = temperature if temperature is not None else config.temperature
        max_tokens = max_tokens if max_tokens is not None else config.max_tokens
        
        # Route to appropriate provider
        start_time = asyncio.get_event_loop().time()
        
        try:
            if config.provider == ModelProvider.OPENAI:
                response = await self._generate_openai_response(
                    messages, config, temperature, max_tokens, **kwargs
                )
            elif config.provider == ModelProvider.CLAUDE:
                response = await self._generate_claude_response(
                    messages, config, temperature, max_tokens, **kwargs
                )
            else:
                raise ValueError(f"Provider '{config.provider.value}' not implemented")
            
            end_time = asyncio.get_event_loop().time()
            response.response_time_ms = int((end_time - start_time) * 1000)
            
            # Record performance metrics
            self.performance_monitor.record_ai_request(
                provider=AIProvider(config.provider.value),
                model=config.model_name,
                endpoint=f"/{config.provider.value}/chat",
                prompt_tokens=response.usage.get('prompt_tokens', 0),
                completion_tokens=response.usage.get('completion_tokens', 0),
                response_time_ms=response.response_time_ms,
                success=True,
                user_id=user_id,
                response_length=len(response.content),
                quality_score=None  # Could add quality assessment later
            )
            
            return response
            
        except Exception as e:
            end_time = asyncio.get_event_loop().time()
            response_time_ms = int((end_time - start_time) * 1000)
            
            # Record failed request
            self.performance_monitor.record_ai_request(
                provider=AIProvider(config.provider.value),
                model=config.model_name,
                endpoint=f"/{config.provider.value}/chat",
                prompt_tokens=0,
                completion_tokens=0,
                response_time_ms=response_time_ms,
                success=False,
                user_id=user_id,
                error_type=type(e).__name__,
                error_message=str(e)
            )
            
            self.logger.error(f"AI generation failed for model {model}: {str(e)}")
            raise
    
    async def _generate_openai_response(
        self,
        messages: List[Dict[str, str]],
        config: AIModelConfig,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> AIProviderResponse:
        """Generate response using OpenAI API"""
        
        client = self.clients[ModelProvider.OPENAI]
        
        response = await client.chat.completions.create(
            model=config.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return AIProviderResponse(
            content=response.choices[0].message.content,
            provider=ModelProvider.OPENAI,
            model=config.model_name,
            usage={
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            },
            response_time_ms=0,  # Will be set by caller
            finish_reason=response.choices[0].finish_reason,
            metadata={
                'response_id': response.id,
                'created': response.created,
                'model': response.model
            }
        )
    
    async def _generate_claude_response(
        self,
        messages: List[Dict[str, str]],
        config: AIModelConfig,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> AIProviderResponse:
        """Generate response using Claude (Anthropic) API"""
        
        client = self.clients[ModelProvider.CLAUDE]
        
        # Convert OpenAI-style messages to Claude format
        claude_messages = self._convert_messages_to_claude_format(messages)
        
        # Extract system message if present
        system_message = None
        if claude_messages and claude_messages[0].get('role') == 'system':
            system_message = claude_messages.pop(0)['content']
        
        # Create Claude request
        request_params = {
            'model': config.model_name,
            'messages': claude_messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        if system_message:
            request_params['system'] = system_message
        
        response = await client.messages.create(**request_params)
        
        # Extract usage information
        usage = {
            'prompt_tokens': response.usage.input_tokens,
            'completion_tokens': response.usage.output_tokens,
            'total_tokens': response.usage.input_tokens + response.usage.output_tokens
        }
        
        return AIProviderResponse(
            content=response.content[0].text,
            provider=ModelProvider.CLAUDE,
            model=config.model_name,
            usage=usage,
            response_time_ms=0,  # Will be set by caller
            finish_reason=response.stop_reason,
            metadata={
                'response_id': response.id,
                'model': response.model,
                'stop_sequence': response.stop_sequence
            }
        )
    
    def _convert_messages_to_claude_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Convert OpenAI-style messages to Claude format"""
        
        claude_messages = []
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            # Claude uses 'user' and 'assistant' roles, system messages handled separately
            if role in ['user', 'assistant', 'system']:
                claude_messages.append({
                    'role': role,
                    'content': content
                })
            else:
                # Convert unknown roles to user messages
                claude_messages.append({
                    'role': 'user',
                    'content': content
                })
        
        return claude_messages
    
    async def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all AI providers"""
        
        status = {}
        
        for provider in ModelProvider:
            provider_status = {
                'available': provider in self.clients,
                'models': [],
                'default_model': None
            }
            
            if provider in self.clients:
                # Get models for this provider
                provider_models = [
                    model_key for model_key, config in self.model_configs.items()
                    if config.provider == provider
                ]
                provider_status['models'] = provider_models
                provider_status['default_model'] = self.get_default_model(provider)
            
            status[provider.value] = provider_status
        
        return status


# Global service instance
_multi_provider_service = None

def get_multi_provider_ai_service() -> MultiProviderAIService:
    """Get the global multi-provider AI service instance"""
    global _multi_provider_service
    
    if _multi_provider_service is None:
        _multi_provider_service = MultiProviderAIService()
    
    return _multi_provider_service


# Export for other modules
__all__ = [
    'MultiProviderAIService',
    'ModelProvider', 
    'AIModelConfig',
    'AIProviderResponse',
    'get_multi_provider_ai_service'
]
