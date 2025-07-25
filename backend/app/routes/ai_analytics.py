"""
Task 2.1.6: AI Analytics API Routes
=================================

API endpoints for AI analytics and quality metrics:
- Analytics dashboard endpoints
- Response quality tracking
- User feedback collection
- Model performance comparison
- Cost and usage analytics
- Trend analysis and reporting
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field

from app.services.ai_analytics_service import (
    get_analytics_service,
    AnalyticsPeriod,
    AnalyticsMetric,
    QualityDimension
)
from app.dependencies import get_current_user
# Import User directly to avoid circular import issues
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["AI Analytics"])


class UserFeedbackRequest(BaseModel):
    """Request model for user feedback"""
    response_id: str = Field(..., description="ID of the AI response")
    user_rating: Optional[float] = Field(None, ge=1.0, le=5.0, description="User rating (1-5 stars)")
    feedback_text: Optional[str] = Field(None, description="User feedback text")


class AnalyticsResponse(BaseModel):
    """Response model for analytics data"""
    period: str
    date_range: Dict[str, str]
    overview: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    usage_metrics: Dict[str, Any]
    cost_metrics: Dict[str, Any]
    model_comparison: List[Dict[str, Any]]
    trends: Dict[str, List]
    generated_at: str


class QualityAnalysisRequest(BaseModel):
    """Request model for quality analysis"""
    response_content: str = Field(..., description="AI response content to analyze")
    prompt_content: str = Field(..., description="Original prompt/query")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")


class QualityAnalysisResponse(BaseModel):
    """Response model for quality analysis"""
    overall_score: float
    dimension_scores: Dict[str, float]
    factors: Dict[str, Any]
    recommendations: List[str]
    analysis_timestamp: str


@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_analytics_dashboard(
    period: str = Query("day", description="Analytics period (hour, day, week, month)"),
    user_id: Optional[str] = Query(None, description="Filter by specific user ID"),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive analytics dashboard data"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period,
            user_id=user_id
        )
        
        return AnalyticsResponse(**dashboard_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics data")


@router.post("/feedback")
async def record_user_feedback(
    feedback: UserFeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    """Record user feedback for an AI response"""
    try:
        analytics_service = await get_analytics_service()
        
        await analytics_service.record_user_feedback(
            response_id=feedback.response_id,
            user_rating=feedback.user_rating,
            feedback=feedback.feedback_text
        )
        
        return {
            "status": "success",
            "message": "User feedback recorded successfully",
            "response_id": feedback.response_id
        }
        
    except Exception as e:
        logger.error(f"Failed to record user feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")


@router.get("/quality/overview")
async def get_quality_overview(
    period: str = Query("day", description="Period for quality overview"),
    current_user: User = Depends(get_current_user)
):
    """Get quality metrics overview"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data and extract quality metrics
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        return {
            "period": period,
            "quality_metrics": dashboard_data["quality_metrics"],
            "overview": {
                "avg_quality_score": dashboard_data["overview"]["avg_quality_score"],
                "avg_user_rating": dashboard_data["overview"]["avg_user_rating"],
                "total_responses": dashboard_data["overview"]["total_responses"]
            },
            "generated_at": dashboard_data["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get quality overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve quality overview")


@router.post("/quality/analyze", response_model=QualityAnalysisResponse)
async def analyze_response_quality(
    request: QualityAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze the quality of an AI response"""
    try:
        analytics_service = await get_analytics_service()
        
        # Calculate quality score
        quality_score = await analytics_service._calculate_quality_score(
            response=request.response_content,
            prompt=request.prompt_content,
            conversation_id=request.conversation_id or "standalone_analysis"
        )
        
        # Generate recommendations based on quality analysis
        recommendations = []
        
        if quality_score.overall_score < 0.6:
            recommendations.append("Consider improving response relevance to the user's query")
        
        if quality_score.dimension_scores.get(QualityDimension.CLARITY, 0) < 0.6:
            recommendations.append("Simplify language and reduce sentence complexity")
        
        if quality_score.dimension_scores.get(QualityDimension.COMPLETENESS, 0) < 0.6:
            recommendations.append("Provide more comprehensive information and examples")
        
        if quality_score.dimension_scores.get(QualityDimension.HELPFULNESS, 0) < 0.6:
            recommendations.append("Include actionable advice and next steps")
        
        if not recommendations:
            recommendations.append("Response quality is good - maintain current standards")
        
        return QualityAnalysisResponse(
            overall_score=quality_score.overall_score,
            dimension_scores={dim.value: score for dim, score in quality_score.dimension_scores.items()},
            factors=quality_score.factors,
            recommendations=recommendations,
            analysis_timestamp=quality_score.calculated_at.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Failed to analyze response quality: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze response quality")


@router.get("/models/comparison")
async def get_model_comparison(
    period: str = Query("day", description="Period for model comparison"),
    current_user: User = Depends(get_current_user)
):
    """Get AI model performance comparison"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data and extract model comparison
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        return {
            "period": period,
            "model_comparison": dashboard_data["model_comparison"],
            "summary": {
                "total_models": len(dashboard_data["model_comparison"]),
                "best_quality": max(dashboard_data["model_comparison"], 
                                  key=lambda x: x["avg_quality_score"], default={}).get("model", "N/A"),
                "fastest": min(dashboard_data["model_comparison"], 
                             key=lambda x: x["avg_response_time"], default={}).get("model", "N/A"),
                "most_cost_effective": min(dashboard_data["model_comparison"], 
                                         key=lambda x: x["avg_cost"], default={}).get("model", "N/A")
            },
            "generated_at": dashboard_data["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model comparison")


@router.get("/usage/stats")
async def get_usage_statistics(
    period: str = Query("day", description="Period for usage statistics"),
    breakdown_by: str = Query("provider", description="Breakdown by: provider, model, user"),
    current_user: User = Depends(get_current_user)
):
    """Get detailed usage statistics"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        usage_metrics = dashboard_data["usage_metrics"]
        
        # Format response based on breakdown type
        if breakdown_by == "provider":
            breakdown_data = usage_metrics.get("provider_distribution", {})
        elif breakdown_by == "model":
            breakdown_data = usage_metrics.get("model_distribution", {})
        else:
            breakdown_data = {}
        
        return {
            "period": period,
            "breakdown_by": breakdown_by,
            "breakdown_data": breakdown_data,
            "summary": {
                "total_responses": dashboard_data["overview"]["total_responses"],
                "personalization_rate": usage_metrics.get("personalization_rate", 0),
                "template_usage_count": len(usage_metrics.get("template_usage", {}))
            },
            "template_usage": usage_metrics.get("template_usage", {}),
            "generated_at": dashboard_data["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get usage statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve usage statistics")


@router.get("/costs/analysis")
async def get_cost_analysis(
    period: str = Query("day", description="Period for cost analysis"),
    current_user: User = Depends(get_current_user)
):
    """Get detailed cost analysis"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        cost_metrics = dashboard_data["cost_metrics"]
        model_comparison = dashboard_data["model_comparison"]
        
        # Calculate cost efficiency metrics
        cost_by_model = {}
        for model in model_comparison:
            cost_by_model[f"{model['provider']}:{model['model']}"] = {
                "avg_cost": model["avg_cost"],
                "total_responses": model["total_responses"],
                "cost_efficiency": model["avg_quality_score"] / max(model["avg_cost"], 0.0001)
            }
        
        return {
            "period": period,
            "cost_summary": cost_metrics,
            "cost_by_model": cost_by_model,
            "efficiency_ranking": sorted(
                cost_by_model.items(),
                key=lambda x: x[1]["cost_efficiency"],
                reverse=True
            )[:5],  # Top 5 most efficient
            "cost_optimization_tips": [
                "Consider using more cost-effective models for simple queries",
                "Implement response caching for repeated questions",
                "Use template-based responses where appropriate",
                "Monitor token usage and optimize prompt lengths"
            ],
            "generated_at": dashboard_data["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get cost analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cost analysis")


@router.get("/trends")
async def get_analytics_trends(
    period: str = Query("week", description="Period for trend analysis"),
    metric: str = Query("quality", description="Metric to track: quality, volume, response_time"),
    current_user: User = Depends(get_current_user)
):
    """Get analytics trends over time"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get dashboard data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        trends = dashboard_data["trends"]
        
        # Select trend data based on metric
        if metric == "quality":
            trend_data = trends.get("quality_trend", [])
        elif metric == "volume":
            trend_data = trends.get("volume_trend", [])
        elif metric == "response_time":
            trend_data = trends.get("response_time_trend", [])
        else:
            raise HTTPException(status_code=400, detail="Invalid metric type")
        
        # Calculate trend analysis
        if len(trend_data) >= 2:
            trend_direction = "increasing" if trend_data[-1] > trend_data[0] else "decreasing"
            trend_change = ((trend_data[-1] - trend_data[0]) / max(trend_data[0], 0.0001)) * 100
        else:
            trend_direction = "stable"
            trend_change = 0
        
        return {
            "period": period,
            "metric": metric,
            "timestamps": trends.get("timestamps", []),
            "trend_data": trend_data,
            "analysis": {
                "direction": trend_direction,
                "change_percent": round(trend_change, 2),
                "current_value": trend_data[-1] if trend_data else 0,
                "average": round(sum(trend_data) / len(trend_data), 2) if trend_data else 0
            },
            "generated_at": dashboard_data["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trends")


@router.get("/health")
async def get_analytics_health():
    """Get analytics service health status"""
    try:
        analytics_service = await get_analytics_service()
        
        # Get basic metrics
        total_responses = len(analytics_service.response_analytics)
        total_conversations = len(analytics_service.conversation_analytics)
        total_models = len(analytics_service.model_performance)
        
        return {
            "status": "healthy",
            "service": "ai_analytics",
            "metrics": {
                "total_responses_tracked": total_responses,
                "total_conversations": total_conversations,
                "models_monitored": total_models,
                "quality_evaluators": len(analytics_service.quality_evaluators)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Analytics health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "ai_analytics",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/export")
async def export_analytics_data(
    period: str = Query("day", description="Period for data export"),
    format: str = Query("json", description="Export format: json, csv"),
    current_user: User = Depends(get_current_user)
):
    """Export analytics data for external analysis"""
    try:
        analytics_service = await get_analytics_service()
        
        # Validate period
        try:
            analytics_period = AnalyticsPeriod(period)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        
        # Get comprehensive dashboard data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=analytics_period
        )
        
        if format == "json":
            return {
                "format": "json",
                "data": dashboard_data,
                "exported_at": datetime.now().isoformat()
            }
        elif format == "csv":
            # For CSV, return a simplified structure
            # In a real implementation, you'd convert to actual CSV format
            return {
                "format": "csv",
                "note": "CSV export would be implemented with proper CSV formatting",
                "preview": {
                    "model_comparison": dashboard_data["model_comparison"],
                    "overview": dashboard_data["overview"]
                },
                "exported_at": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="Unsupported export format")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export analytics data: {e}")
        raise HTTPException(status_code=500, detail="Failed to export data")


# Additional endpoint for real-time analytics updates
@router.get("/realtime/metrics")
async def get_realtime_metrics(
    current_user: User = Depends(get_current_user)
):
    """Get real-time analytics metrics (last hour)"""
    try:
        analytics_service = await get_analytics_service()
        
        # Get last hour data
        dashboard_data = await analytics_service.get_analytics_dashboard(
            period=AnalyticsPeriod.HOUR
        )
        
        # Extract key real-time metrics
        return {
            "current_hour": {
                "total_responses": dashboard_data["overview"]["total_responses"],
                "avg_quality_score": dashboard_data["overview"]["avg_quality_score"],
                "avg_response_time": dashboard_data["performance_metrics"].get("avg_response_time", 0),
                "active_users": dashboard_data["overview"]["unique_users"]
            },
            "live_trends": {
                "last_5_responses": dashboard_data["trends"]["volume_trend"][-5:] if len(dashboard_data["trends"]["volume_trend"]) >= 5 else dashboard_data["trends"]["volume_trend"],
                "quality_trend": dashboard_data["trends"]["quality_trend"][-5:] if len(dashboard_data["trends"]["quality_trend"]) >= 5 else dashboard_data["trends"]["quality_trend"]
            },
            "alerts": [],  # Could add threshold-based alerts here
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get real-time metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve real-time metrics")
