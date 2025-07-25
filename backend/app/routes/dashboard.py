"""
Performance Dashboard API Routes for Task 1.3.4
===============================================

API endpoints for the real-time performance dashboard:
- Dashboard data aggregation
- Real-time system metrics
- Performance visualizations
- Alert management
- Historical trend analysis
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import json
import asyncio

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.services.dashboard_service import get_dashboard_service, DashboardWidget, DashboardData

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Pydantic models for API responses
class DashboardWidgetResponse(BaseModel):
    """Response model for dashboard widgets"""
    id: str
    title: str
    type: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[str] = None
    status: Optional[str] = None
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    """Response model for complete dashboard"""
    timestamp: str
    system_status: str
    widgets: List[DashboardWidgetResponse]
    alerts: List[Dict[str, Any]]
    performance_summary: Dict[str, Any]
    trends: Dict[str, Any]

    class Config:
        from_attributes = True


class RealTimeDashboardResponse(BaseModel):
    """Response model for real-time dashboard data"""
    timestamp: str
    system_status: str
    quick_stats: Dict[str, Any]
    system_health: Dict[str, Any]
    alerts_count: int
    recent_activity: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class PerformanceChartsResponse(BaseModel):
    """Response model for performance charts"""
    time_buckets: List[str]
    system_resources: Dict[str, List[float]]
    request_volume: List[float]
    error_rate: List[float]
    response_times: List[float]

    class Config:
        from_attributes = True


class EndpointAnalyticsResponse(BaseModel):
    """Response model for endpoint analytics"""
    timestamp: str
    total_endpoints: int
    top_by_volume: List[Dict[str, Any]]
    top_by_errors: List[Dict[str, Any]]
    slowest_endpoints: List[Dict[str, Any]]

    class Config:
        from_attributes = True


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    time_window: int = Query(24, ge=1, le=168, description="Time window in hours (max 1 week)")
):
    """
    Get complete performance dashboard data
    
    Returns comprehensive dashboard including:
    - System status widgets
    - Performance metrics
    - Active alerts
    - Trend analysis
    - Performance summary
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    dashboard_data = await dashboard_service.get_dashboard_data(time_window)
    
    # Convert widgets to response format
    widget_responses = [
        DashboardWidgetResponse(**widget.__dict__)
        for widget in dashboard_data.widgets
    ]
    
    return DashboardResponse(
        timestamp=dashboard_data.timestamp,
        system_status=dashboard_data.system_status,
        widgets=widget_responses,
        alerts=dashboard_data.alerts,
        performance_summary=dashboard_data.performance_summary,
        trends=dashboard_data.trends
    )


@router.get("/real-time", response_model=RealTimeDashboardResponse)
async def get_real_time_dashboard(
    current_user: User = Depends(get_current_user)
):
    """
    Get real-time dashboard data
    
    Returns current system state with minimal latency:
    - Live system metrics
    - Current request rates
    - Active alerts count
    - Recent activity
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    real_time_data = await dashboard_service.get_real_time_dashboard()
    
    return RealTimeDashboardResponse(**real_time_data)


@router.get("/stream")
async def get_dashboard_stream(
    current_user: User = Depends(get_current_user)
):
    """
    Stream real-time dashboard updates via Server-Sent Events
    
    Provides continuous dashboard updates for real-time monitoring
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    
    async def event_stream():
        """Generate server-sent events for dashboard updates"""
        while True:
            try:
                # Get real-time data
                real_time_data = await dashboard_service.get_real_time_dashboard()
                
                # Format as SSE
                data = json.dumps(real_time_data)
                yield f"data: {data}\n\n"
                
                # Wait 5 seconds before next update
                await asyncio.sleep(5)
                
            except Exception as e:
                # Send error event
                error_data = {
                    "error": True,
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                await asyncio.sleep(10)  # Wait longer on error
    
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


@router.get("/charts", response_model=PerformanceChartsResponse)
async def get_performance_charts(
    current_user: User = Depends(get_current_user),
    hours: int = Query(24, ge=1, le=168, description="Time window in hours")
):
    """
    Get performance chart data for visualization
    
    Returns time-series data for:
    - System resource usage
    - Request volume patterns
    - Error rate trends
    - Response time patterns
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    charts_data = await dashboard_service.get_performance_charts(hours)
    
    return PerformanceChartsResponse(**charts_data)


@router.get("/analytics/endpoints", response_model=EndpointAnalyticsResponse)
async def get_endpoint_analytics(
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed endpoint performance analytics
    
    Returns endpoint-specific performance data:
    - Top endpoints by volume
    - Endpoints with highest error rates
    - Slowest performing endpoints
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    analytics_data = await dashboard_service.get_endpoint_analytics()
    
    return EndpointAnalyticsResponse(**analytics_data)


@router.get("/widgets")
async def get_dashboard_widgets(
    current_user: User = Depends(get_current_user),
    widget_types: Optional[str] = Query(None, description="Comma-separated widget types to include")
):
    """
    Get specific dashboard widgets
    
    Allows fetching only specific widget types:
    - system: System resource widgets
    - performance: Performance metric widgets
    - errors: Error tracking widgets
    - health: Health status widgets
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    dashboard_data = await dashboard_service.get_dashboard_data()
    
    # Filter widgets by type if specified
    widgets = dashboard_data.widgets
    if widget_types:
        requested_types = [t.strip() for t in widget_types.split(",")]
        widgets = [w for w in widgets if any(t in w.id for t in requested_types)]
    
    widget_responses = [
        DashboardWidgetResponse(**widget.__dict__)
        for widget in widgets
    ]
    
    return {
        "widgets": widget_responses,
        "timestamp": dashboard_data.timestamp,
        "total_widgets": len(widget_responses)
    }


@router.get("/alerts")
async def get_dashboard_alerts(
    current_user: User = Depends(get_current_user),
    severity: Optional[str] = Query(None, description="Filter by alert severity")
):
    """
    Get active dashboard alerts
    
    Returns current system alerts with optional filtering:
    - All active alerts
    - Filter by severity level
    - Alert metadata and recommendations
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    dashboard_data = await dashboard_service.get_dashboard_data()
    
    alerts = dashboard_data.alerts
    
    # Filter by severity if specified
    if severity:
        severity_levels = [s.strip().lower() for s in severity.split(",")]
        alerts = [a for a in alerts if a.get("severity", "").lower() in severity_levels]
    
    return {
        "alerts": alerts,
        "alert_count": len(alerts),
        "highest_severity": max([a.get("severity", "low") for a in alerts], default="none"),
        "timestamp": dashboard_data.timestamp
    }


@router.get("/health-summary")
async def get_health_summary(
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard health summary
    
    Returns overall system health for dashboard header:
    - System status
    - Key health indicators
    - Critical alerts count
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    dashboard_service = get_dashboard_service()
    real_time_data = await dashboard_service.get_real_time_dashboard()
    
    # Calculate health score based on various factors
    health_score = 100
    
    # Reduce score based on system metrics
    cpu_percent = real_time_data["system_health"]["cpu_percent"]
    memory_percent = real_time_data["system_health"]["memory_percent"]
    error_rate = real_time_data["quick_stats"]["error_rate"]
    
    if cpu_percent > 80:
        health_score -= 20
    elif cpu_percent > 70:
        health_score -= 10
    
    if memory_percent > 85:
        health_score -= 20
    elif memory_percent > 75:
        health_score -= 10
    
    if error_rate > 5:
        health_score -= 30
    elif error_rate > 2:
        health_score -= 15
    
    health_score = max(0, health_score)
    
    # Determine overall status
    if health_score >= 90:
        overall_status = "excellent"
    elif health_score >= 75:
        overall_status = "good"
    elif health_score >= 50:
        overall_status = "fair"
    else:
        overall_status = "poor"
    
    return {
        "system_status": real_time_data["system_status"],
        "overall_status": overall_status,
        "health_score": health_score,
        "critical_alerts": real_time_data["alerts_count"],
        "key_metrics": {
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory_percent}%",
            "error_rate": f"{error_rate}%",
            "requests_per_minute": real_time_data["quick_stats"]["requests_per_minute"]
        },
        "timestamp": real_time_data["timestamp"]
    }


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Acknowledge a dashboard alert
    
    Marks an alert as acknowledged by the current user
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    # This would typically update alert status in a database
    # For now, return success response
    return {
        "alert_id": alert_id,
        "acknowledged": True,
        "acknowledged_by": current_user.email,
        "acknowledged_at": datetime.utcnow().isoformat(),
        "message": "Alert acknowledged successfully"
    }


@router.get("/export")
async def export_dashboard_data(
    current_user: User = Depends(get_current_user),
    format: str = Query("json", description="Export format (json, csv)"),
    time_window: int = Query(24, ge=1, le=168, description="Time window in hours")
):
    """
    Export dashboard data for analysis
    
    Exports comprehensive dashboard data in various formats:
    - JSON format for API integration
    - CSV format for spreadsheet analysis
    """
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    dashboard_service = get_dashboard_service()
    dashboard_data = await dashboard_service.get_dashboard_data(time_window)
    
    if format.lower() == "json":
        # Export as JSON
        export_data = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "time_window_hours": time_window,
            "dashboard_data": {
                "timestamp": dashboard_data.timestamp,
                "system_status": dashboard_data.system_status,
                "widgets": [widget.__dict__ for widget in dashboard_data.widgets],
                "alerts": dashboard_data.alerts,
                "performance_summary": dashboard_data.performance_summary,
                "trends": dashboard_data.trends
            }
        }
        
        return export_data
    
    elif format.lower() == "csv":
        # Export widget data as CSV
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(["Widget ID", "Title", "Type", "Value", "Unit", "Status", "Trend"])
        
        # Write widget data
        for widget in dashboard_data.widgets:
            writer.writerow([
                widget.id,
                widget.title,
                widget.type,
                widget.value,
                widget.unit or "",
                widget.status or "",
                widget.trend or ""
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported export format. Use 'json' or 'csv'"
        )
