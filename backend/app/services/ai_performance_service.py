"""
AI Performance Metrics Service for Task 1.3.2
=============================================

Comprehensive AI service performance monitoring:
- OpenAI API usage tracking (tokens, costs, response times)
- AI service health monitoring and availability
- Performance analytics and optimization insights
- Usage pattern analysis and forecasting
- Cost management and billing analytics
- Integration with monitoring and alert systems
"""

import logging
import time
import asyncio
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import json
import os
from statistics import mean, median

from sqlalchemy.orm import Session
from app.database import get_db
from app.services.audit_service import get_audit_logger, AuditEventType, AuditLogLevel
from app.services.error_tracker import get_error_tracker


class AIProvider(Enum):
    """AI service providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    CUSTOM = "custom"


class AIMetricType(Enum):
    """Types of AI metrics"""
    TOKEN_USAGE = "token_usage"
    RESPONSE_TIME = "response_time"
    COST = "cost"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    QUALITY_SCORE = "quality_score"


@dataclass
class AIUsageMetrics:
    """AI service usage metrics"""
    timestamp: datetime
    provider: AIProvider
    model: str
    endpoint: str
    user_id: Optional[str]
    
    # Token metrics
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    # Performance metrics
    response_time_ms: int
    success: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    
    # Cost metrics
    estimated_cost: float = 0.0
    
    # Quality metrics
    response_length: int = 0
    quality_score: Optional[float] = None
    
    # Request metadata
    request_id: Optional[str] = None
    session_id: Optional[str] = None
    client_ip: Optional[str] = None


@dataclass
class AIPerformanceStats:
    """Aggregated AI performance statistics"""
    time_period: str
    provider: AIProvider
    model: str
    
    # Usage statistics
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    
    # Token statistics
    total_tokens: int
    avg_tokens_per_request: float
    prompt_tokens: int
    completion_tokens: int
    
    # Performance statistics
    avg_response_time_ms: float
    median_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    
    # Cost statistics
    total_cost: float
    cost_per_request: float
    cost_per_token: float
    
    # Error analysis
    error_breakdown: Dict[str, int]
    error_rate: float


class AIPerformanceMonitor:
    """Comprehensive AI performance monitoring system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audit_logger = get_audit_logger()
        self.error_tracker = get_error_tracker()
        
        # Metrics storage
        self.metrics_history = deque(maxlen=10000)  # Keep last 10k metrics
        self.real_time_metrics = defaultdict(list)
        
        # Performance tracking
        self.response_times = defaultdict(lambda: deque(maxlen=1000))
        self.token_usage = defaultdict(lambda: {"prompt": 0, "completion": 0, "total": 0})
        self.cost_tracking = defaultdict(float)
        self.error_counts = defaultdict(int)
        
        # Rate limiting tracking
        self.rate_limit_status = {}
        
        # Load AI service configurations
        self.ai_configs = self._load_ai_configurations()
        
        # Initialize cost calculation models
        self.cost_models = self._initialize_cost_models()
        
        self.logger.info("AI Performance Monitor initialized")
    
    def _load_ai_configurations(self) -> Dict[str, Any]:
        """Load AI service configurations"""
        return {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "organization": os.getenv("OPENAI_ORG_ID", ""),
                "base_url": "https://api.openai.com/v1",
                "timeout": 30,
                "max_retries": 3
            },
            "claude": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "base_url": "https://api.anthropic.com/v1",
                "timeout": 30
            },
            "gemini": {
                "api_key": os.getenv("GOOGLE_AI_API_KEY", ""),
                "base_url": "https://generativelanguage.googleapis.com/v1",
                "timeout": 30
            }
        }
    
    def _initialize_cost_models(self) -> Dict[str, Dict[str, float]]:
        """Initialize cost calculation models for different AI providers"""
        return {
            "openai": {
                "gpt-4": {
                    "prompt_cost_per_1k": 0.03,
                    "completion_cost_per_1k": 0.06
                },
                "gpt-4-turbo": {
                    "prompt_cost_per_1k": 0.01,
                    "completion_cost_per_1k": 0.03
                },
                "gpt-3.5-turbo": {
                    "prompt_cost_per_1k": 0.0015,
                    "completion_cost_per_1k": 0.002
                },
                "gpt-3.5-turbo-instruct": {
                    "prompt_cost_per_1k": 0.0015,
                    "completion_cost_per_1k": 0.002
                }
            },
            "claude": {
                "claude-3-opus": {
                    "prompt_cost_per_1k": 0.015,
                    "completion_cost_per_1k": 0.075
                },
                "claude-3-sonnet": {
                    "prompt_cost_per_1k": 0.003,
                    "completion_cost_per_1k": 0.015
                },
                "claude-3-haiku": {
                    "prompt_cost_per_1k": 0.00025,
                    "completion_cost_per_1k": 0.00125
                }
            },
            "gemini": {
                "gemini-pro": {
                    "prompt_cost_per_1k": 0.0005,
                    "completion_cost_per_1k": 0.0015
                },
                "gemini-pro-vision": {
                    "prompt_cost_per_1k": 0.0025,
                    "completion_cost_per_1k": 0.01
                }
            }
        }
    
    def calculate_cost(self, 
                      provider: AIProvider, 
                      model: str, 
                      prompt_tokens: int, 
                      completion_tokens: int) -> float:
        """Calculate estimated cost for AI request"""
        
        try:
            cost_model = self.cost_models.get(provider.value, {}).get(model, {})
            
            if not cost_model:
                self.logger.warning(f"No cost model found for {provider.value}/{model}")
                return 0.0
            
            prompt_cost = (prompt_tokens / 1000) * cost_model.get("prompt_cost_per_1k", 0)
            completion_cost = (completion_tokens / 1000) * cost_model.get("completion_cost_per_1k", 0)
            
            return prompt_cost + completion_cost
            
        except Exception as e:
            self.logger.error(f"Error calculating cost: {str(e)}")
            return 0.0
    
    def record_ai_request(self,
                         provider: AIProvider,
                         model: str,
                         endpoint: str,
                         prompt_tokens: int,
                         completion_tokens: int,
                         response_time_ms: int,
                         success: bool,
                         user_id: Optional[str] = None,
                         error_type: Optional[str] = None,
                         error_message: Optional[str] = None,
                         response_length: int = 0,
                         quality_score: Optional[float] = None,
                         request_id: Optional[str] = None,
                         session_id: Optional[str] = None,
                         client_ip: Optional[str] = None) -> str:
        """Record AI service request metrics"""
        
        try:
            total_tokens = prompt_tokens + completion_tokens
            estimated_cost = self.calculate_cost(provider, model, prompt_tokens, completion_tokens)
            
            # Create metrics record
            metrics = AIUsageMetrics(
                timestamp=datetime.utcnow(),
                provider=provider,
                model=model,
                endpoint=endpoint,
                user_id=user_id,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                response_time_ms=response_time_ms,
                success=success,
                error_type=error_type,
                error_message=error_message,
                estimated_cost=estimated_cost,
                response_length=response_length,
                quality_score=quality_score,
                request_id=request_id,
                session_id=session_id,
                client_ip=client_ip
            )
            
            # Store metrics
            self.metrics_history.append(metrics)
            
            # Update real-time tracking
            key = f"{provider.value}_{model}"
            self.real_time_metrics[key].append(metrics)
            
            # Update performance tracking
            self.response_times[key].append(response_time_ms)
            
            # Update token usage
            self.token_usage[key]["prompt"] += prompt_tokens
            self.token_usage[key]["completion"] += completion_tokens
            self.token_usage[key]["total"] += total_tokens
            
            # Update cost tracking
            self.cost_tracking[key] += estimated_cost
            
            # Track errors
            if not success and error_type:
                self.error_counts[f"{key}_{error_type}"] += 1
            
            # Log to audit system
            try:
                db = next(get_db())
                self.audit_logger.log_event(
                    db=db,
                    event_type=AuditEventType.AI_PROMPT_SUBMITTED,
                    event_category="ai_performance",
                    user_id=user_id,
                    event_description=f"AI request to {provider.value}/{model}",
                    success=success,
                    error_message=error_message,
                    metadata={
                        "provider": provider.value,
                        "model": model,
                        "endpoint": endpoint,
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": total_tokens,
                        "response_time_ms": response_time_ms,
                        "estimated_cost": estimated_cost,
                        "quality_score": quality_score
                    },
                    event_level=AuditLogLevel.ERROR if not success else AuditLogLevel.INFO
                )
            except Exception as e:
                self.logger.error(f"Failed to log AI metrics to audit system: {str(e)}")
            
            # Generate metrics ID
            metrics_id = f"{provider.value}_{model}_{int(time.time() * 1000)}"
            
            self.logger.debug(f"Recorded AI metrics: {metrics_id}")
            return metrics_id
            
        except Exception as e:
            self.logger.error(f"Error recording AI request metrics: {str(e)}")
            return ""
    
    def get_performance_stats(self,
                            provider: Optional[AIProvider] = None,
                            model: Optional[str] = None,
                            time_period: str = "1h") -> Dict[str, AIPerformanceStats]:
        """Get aggregated performance statistics"""
        
        try:
            # Calculate time range
            time_delta = self._parse_time_period(time_period)
            cutoff_time = datetime.utcnow() - time_delta
            
            # Filter metrics by time period
            filtered_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= cutoff_time
            ]
            
            # Filter by provider and model if specified
            if provider:
                filtered_metrics = [m for m in filtered_metrics if m.provider == provider]
            if model:
                filtered_metrics = [m for m in filtered_metrics if m.model == model]
            
            # Group metrics by provider and model
            grouped_metrics = defaultdict(list)
            for metric in filtered_metrics:
                key = f"{metric.provider.value}_{metric.model}"
                grouped_metrics[key].append(metric)
            
            # Calculate statistics for each group
            stats = {}
            for key, metrics_list in grouped_metrics.items():
                if not metrics_list:
                    continue
                
                provider_name, model_name = key.split("_", 1)
                provider_enum = AIProvider(provider_name)
                
                # Calculate aggregated statistics
                stats[key] = self._calculate_group_stats(
                    metrics_list, provider_enum, model_name, time_period
                )
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting performance stats: {str(e)}")
            return {}
    
    def _parse_time_period(self, time_period: str) -> timedelta:
        """Parse time period string to timedelta"""
        
        if time_period.endswith('m'):
            return timedelta(minutes=int(time_period[:-1]))
        elif time_period.endswith('h'):
            return timedelta(hours=int(time_period[:-1]))
        elif time_period.endswith('d'):
            return timedelta(days=int(time_period[:-1]))
        else:
            # Default to 1 hour
            return timedelta(hours=1)
    
    def _calculate_group_stats(self,
                              metrics_list: List[AIUsageMetrics],
                              provider: AIProvider,
                              model: str,
                              time_period: str) -> AIPerformanceStats:
        """Calculate statistics for a group of metrics"""
        
        total_requests = len(metrics_list)
        successful_requests = len([m for m in metrics_list if m.success])
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        
        # Token statistics
        total_tokens = sum(m.total_tokens for m in metrics_list)
        prompt_tokens = sum(m.prompt_tokens for m in metrics_list)
        completion_tokens = sum(m.completion_tokens for m in metrics_list)
        avg_tokens_per_request = total_tokens / total_requests if total_requests > 0 else 0
        
        # Response time statistics
        response_times = [m.response_time_ms for m in metrics_list if m.response_time_ms > 0]
        avg_response_time_ms = mean(response_times) if response_times else 0
        median_response_time_ms = median(response_times) if response_times else 0
        
        # Calculate percentiles
        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95) if sorted_times else 0
        p99_index = int(len(sorted_times) * 0.99) if sorted_times else 0
        p95_response_time_ms = sorted_times[p95_index] if p95_index < len(sorted_times) else 0
        p99_response_time_ms = sorted_times[p99_index] if p99_index < len(sorted_times) else 0
        
        # Cost statistics
        total_cost = sum(m.estimated_cost for m in metrics_list)
        cost_per_request = total_cost / total_requests if total_requests > 0 else 0
        cost_per_token = total_cost / total_tokens if total_tokens > 0 else 0
        
        # Error analysis
        error_breakdown = defaultdict(int)
        for metric in metrics_list:
            if not metric.success and metric.error_type:
                error_breakdown[metric.error_type] += 1
        
        error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0
        
        return AIPerformanceStats(
            time_period=time_period,
            provider=provider,
            model=model,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            success_rate=success_rate,
            total_tokens=total_tokens,
            avg_tokens_per_request=avg_tokens_per_request,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            avg_response_time_ms=avg_response_time_ms,
            median_response_time_ms=median_response_time_ms,
            p95_response_time_ms=p95_response_time_ms,
            p99_response_time_ms=p99_response_time_ms,
            total_cost=total_cost,
            cost_per_request=cost_per_request,
            cost_per_token=cost_per_token,
            error_breakdown=dict(error_breakdown),
            error_rate=error_rate
        )
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time AI performance metrics"""
        
        try:
            current_time = datetime.utcnow()
            one_minute_ago = current_time - timedelta(minutes=1)
            five_minutes_ago = current_time - timedelta(minutes=5)
            
            # Get recent metrics
            recent_1m = [m for m in self.metrics_history if m.timestamp >= one_minute_ago]
            recent_5m = [m for m in self.metrics_history if m.timestamp >= five_minutes_ago]
            
            return {
                "timestamp": current_time.isoformat(),
                "metrics_1m": {
                    "total_requests": len(recent_1m),
                    "successful_requests": len([m for m in recent_1m if m.success]),
                    "failed_requests": len([m for m in recent_1m if not m.success]),
                    "avg_response_time": mean([m.response_time_ms for m in recent_1m]) if recent_1m else 0,
                    "total_tokens": sum(m.total_tokens for m in recent_1m),
                    "total_cost": sum(m.estimated_cost for m in recent_1m)
                },
                "metrics_5m": {
                    "total_requests": len(recent_5m),
                    "successful_requests": len([m for m in recent_5m if m.success]),
                    "failed_requests": len([m for m in recent_5m if not m.success]),
                    "avg_response_time": mean([m.response_time_ms for m in recent_5m]) if recent_5m else 0,
                    "total_tokens": sum(m.total_tokens for m in recent_5m),
                    "total_cost": sum(m.estimated_cost for m in recent_5m)
                },
                "active_providers": list(set(m.provider.value for m in recent_5m)),
                "active_models": list(set(f"{m.provider.value}/{m.model}" for m in recent_5m))
            }
            
        except Exception as e:
            self.logger.error(f"Error getting real-time metrics: {str(e)}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
    
    def get_cost_analytics(self, time_period: str = "24h") -> Dict[str, Any]:
        """Get detailed cost analytics"""
        
        try:
            time_delta = self._parse_time_period(time_period)
            cutoff_time = datetime.utcnow() - time_delta
            
            # Filter metrics by time period
            filtered_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= cutoff_time
            ]
            
            # Cost breakdown by provider
            cost_by_provider = defaultdict(float)
            cost_by_model = defaultdict(float)
            cost_by_user = defaultdict(float)
            
            for metric in filtered_metrics:
                provider_key = metric.provider.value
                model_key = f"{metric.provider.value}/{metric.model}"
                user_key = metric.user_id or "anonymous"
                
                cost_by_provider[provider_key] += metric.estimated_cost
                cost_by_model[model_key] += metric.estimated_cost
                cost_by_user[user_key] += metric.estimated_cost
            
            # Token usage breakdown
            token_usage_by_provider = defaultdict(lambda: {"prompt": 0, "completion": 0, "total": 0})
            for metric in filtered_metrics:
                provider_key = metric.provider.value
                token_usage_by_provider[provider_key]["prompt"] += metric.prompt_tokens
                token_usage_by_provider[provider_key]["completion"] += metric.completion_tokens
                token_usage_by_provider[provider_key]["total"] += metric.total_tokens
            
            total_cost = sum(cost_by_provider.values())
            total_requests = len(filtered_metrics)
            
            return {
                "time_period": time_period,
                "total_cost": total_cost,
                "total_requests": total_requests,
                "cost_per_request": total_cost / total_requests if total_requests > 0 else 0,
                "cost_by_provider": dict(cost_by_provider),
                "cost_by_model": dict(cost_by_model),
                "cost_by_user": dict(cost_by_user),
                "token_usage_by_provider": dict(token_usage_by_provider),
                "top_cost_users": sorted(
                    cost_by_user.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10],
                "top_cost_models": sorted(
                    cost_by_model.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting cost analytics: {str(e)}")
            return {"error": str(e)}
    
    def get_usage_patterns(self, time_period: str = "24h") -> Dict[str, Any]:
        """Analyze AI usage patterns"""
        
        try:
            time_delta = self._parse_time_period(time_period)
            cutoff_time = datetime.utcnow() - time_delta
            
            # Filter metrics by time period
            filtered_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= cutoff_time
            ]
            
            # Usage patterns by hour
            hourly_usage = defaultdict(int)
            hourly_cost = defaultdict(float)
            
            for metric in filtered_metrics:
                hour = metric.timestamp.hour
                hourly_usage[hour] += 1
                hourly_cost[hour] += metric.estimated_cost
            
            # Most active users
            user_activity = defaultdict(lambda: {"requests": 0, "tokens": 0, "cost": 0})
            for metric in filtered_metrics:
                user_key = metric.user_id or "anonymous"
                user_activity[user_key]["requests"] += 1
                user_activity[user_key]["tokens"] += metric.total_tokens
                user_activity[user_key]["cost"] += metric.estimated_cost
            
            # Model popularity
            model_usage = defaultdict(int)
            for metric in filtered_metrics:
                model_key = f"{metric.provider.value}/{metric.model}"
                model_usage[model_key] += 1
            
            return {
                "time_period": time_period,
                "total_requests": len(filtered_metrics),
                "unique_users": len(set(m.user_id for m in filtered_metrics if m.user_id)),
                "hourly_usage": dict(hourly_usage),
                "hourly_cost": dict(hourly_cost),
                "peak_hour": max(hourly_usage.items(), key=lambda x: x[1])[0] if hourly_usage else None,
                "most_active_users": sorted(
                    user_activity.items(), 
                    key=lambda x: x[1]["requests"], 
                    reverse=True
                )[:10],
                "most_popular_models": sorted(
                    model_usage.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing usage patterns: {str(e)}")
            return {"error": str(e)}
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get AI service health status"""
        
        try:
            current_time = datetime.utcnow()
            five_minutes_ago = current_time - timedelta(minutes=5)
            
            # Get recent metrics
            recent_metrics = [m for m in self.metrics_history if m.timestamp >= five_minutes_ago]
            
            if not recent_metrics:
                return {
                    "status": "no_data",
                    "message": "No recent AI service activity",
                    "timestamp": current_time.isoformat()
                }
            
            # Calculate health indicators
            total_requests = len(recent_metrics)
            successful_requests = len([m for m in recent_metrics if m.success])
            success_rate = (successful_requests / total_requests) * 100
            
            avg_response_time = mean([m.response_time_ms for m in recent_metrics])
            
            # Determine health status
            if success_rate >= 99 and avg_response_time < 2000:
                status = "healthy"
            elif success_rate >= 95 and avg_response_time < 5000:
                status = "warning"
            else:
                status = "critical"
            
            # Provider-specific health
            provider_health = {}
            for provider in AIProvider:
                provider_metrics = [m for m in recent_metrics if m.provider == provider]
                if provider_metrics:
                    provider_success_rate = (
                        len([m for m in provider_metrics if m.success]) / len(provider_metrics)
                    ) * 100
                    provider_avg_response_time = mean([m.response_time_ms for m in provider_metrics])
                    
                    provider_health[provider.value] = {
                        "requests": len(provider_metrics),
                        "success_rate": provider_success_rate,
                        "avg_response_time": provider_avg_response_time,
                        "status": "healthy" if provider_success_rate >= 95 else "degraded"
                    }
            
            return {
                "status": status,
                "overall_success_rate": success_rate,
                "avg_response_time_ms": avg_response_time,
                "total_requests_5m": total_requests,
                "successful_requests_5m": successful_requests,
                "provider_health": provider_health,
                "timestamp": current_time.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI health status: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get AI performance optimization recommendations"""
        
        try:
            recommendations = []
            
            # Analyze recent performance
            stats_24h = self.get_performance_stats(time_period="24h")
            cost_analytics = self.get_cost_analytics(time_period="24h")
            
            for key, stats in stats_24h.items():
                provider, model = key.split("_", 1)
                
                # High response time recommendation
                if stats.avg_response_time_ms > 3000:
                    recommendations.append({
                        "type": "performance",
                        "priority": "high",
                        "provider": provider,
                        "model": model,
                        "issue": "high_response_time",
                        "description": f"Average response time of {stats.avg_response_time_ms:.0f}ms is above optimal threshold",
                        "recommendation": "Consider using a faster model or implementing request caching",
                        "impact": "Improved user experience and reduced latency"
                    })
                
                # High error rate recommendation
                if stats.error_rate > 5:
                    recommendations.append({
                        "type": "reliability",
                        "priority": "critical",
                        "provider": provider,
                        "model": model,
                        "issue": "high_error_rate",
                        "description": f"Error rate of {stats.error_rate:.1f}% is above acceptable threshold",
                        "recommendation": "Investigate error patterns and implement retry logic",
                        "impact": "Improved service reliability and user satisfaction"
                    })
                
                # High cost per request recommendation
                if stats.cost_per_request > 0.1:
                    recommendations.append({
                        "type": "cost",
                        "priority": "medium",
                        "provider": provider,
                        "model": model,
                        "issue": "high_cost_per_request",
                        "description": f"Cost per request of ${stats.cost_per_request:.4f} is above optimal range",
                        "recommendation": "Consider using a more cost-effective model or optimizing prompts",
                        "impact": "Reduced operational costs"
                    })
                
                # Token usage optimization
                if stats.avg_tokens_per_request > 2000:
                    recommendations.append({
                        "type": "efficiency",
                        "priority": "medium",
                        "provider": provider,
                        "model": model,
                        "issue": "high_token_usage",
                        "description": f"Average of {stats.avg_tokens_per_request:.0f} tokens per request is high",
                        "recommendation": "Optimize prompts to reduce token consumption",
                        "impact": "Lower costs and faster response times"
                    })
            
            # Sort recommendations by priority
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating optimization recommendations: {str(e)}")
            return []


# Global AI performance monitor instance
_ai_performance_monitor = None

def get_ai_performance_monitor() -> AIPerformanceMonitor:
    """Get global AI performance monitor instance"""
    global _ai_performance_monitor
    if _ai_performance_monitor is None:
        _ai_performance_monitor = AIPerformanceMonitor()
    return _ai_performance_monitor


# Decorator for AI function monitoring
def monitor_ai_performance(provider: AIProvider, model: str, endpoint: str):
    """Decorator to automatically monitor AI function performance"""
    
    def decorator(func: Callable) -> Callable:
        async def async_wrapper(*args, **kwargs):
            monitor = get_ai_performance_monitor()
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                
                # Extract metrics from result (assuming standard format)
                response_time_ms = int((time.time() - start_time) * 1000)
                prompt_tokens = getattr(result, 'prompt_tokens', 0)
                completion_tokens = getattr(result, 'completion_tokens', 0)
                
                # Record successful request
                monitor.record_ai_request(
                    provider=provider,
                    model=model,
                    endpoint=endpoint,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time_ms=response_time_ms,
                    success=True
                )
                
                return result
                
            except Exception as e:
                # Record failed request
                response_time_ms = int((time.time() - start_time) * 1000)
                
                monitor.record_ai_request(
                    provider=provider,
                    model=model,
                    endpoint=endpoint,
                    prompt_tokens=0,
                    completion_tokens=0,
                    response_time_ms=response_time_ms,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                
                raise
        
        def sync_wrapper(*args, **kwargs):
            monitor = get_ai_performance_monitor()
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Extract metrics from result
                response_time_ms = int((time.time() - start_time) * 1000)
                prompt_tokens = getattr(result, 'prompt_tokens', 0)
                completion_tokens = getattr(result, 'completion_tokens', 0)
                
                # Record successful request
                monitor.record_ai_request(
                    provider=provider,
                    model=model,
                    endpoint=endpoint,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    response_time_ms=response_time_ms,
                    success=True
                )
                
                return result
                
            except Exception as e:
                # Record failed request
                response_time_ms = int((time.time() - start_time) * 1000)
                
                monitor.record_ai_request(
                    provider=provider,
                    model=model,
                    endpoint=endpoint,
                    prompt_tokens=0,
                    completion_tokens=0,
                    response_time_ms=response_time_ms,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator
