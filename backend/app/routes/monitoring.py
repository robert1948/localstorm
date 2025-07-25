"""
Monitoring API Routes for Task 1.3.1 - Real-time Metrics Collection
===================================================================

API endpoints for accessing monitoring data, metrics, and system health:
- Real-time metrics retrieval
- System health monitoring
- Performance analytics
- Error tracking and statistics
- Custom business metrics
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.middleware.monitoring import (
    health_check_detailed,
    get_metrics_summary,
    get_real_time_metrics,
    metrics_collector
)

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


# Pydantic models for API responses
class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: str
    issues: List[str] = []
    system: Dict[str, Any]
    application: Dict[str, Any]
    metrics_summary: Dict[str, Any]

    class Config:
        from_attributes = True


class MetricsSummaryResponse(BaseModel):
    """Response model for metrics summary"""
    timestamp: str
    performance: Dict[str, Any]
    system: Dict[str, Any]
    endpoints: Dict[str, Any]
    status_codes: Dict[str, Any]
    recent_requests: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class RealTimeMetricsResponse(BaseModel):
    """Response model for real-time metrics"""
    time_window_minutes: int
    metrics: Dict[str, List[Dict[str, Any]]]
    summary: Dict[str, Any]

    class Config:
        from_attributes = True


class SystemStatsResponse(BaseModel):
    """Response model for system statistics"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_average: Optional[List[float]]
    uptime_seconds: float
    active_connections: int

    class Config:
        from_attributes = True


@router.get("/health", response_model=HealthCheckResponse)
async def get_health_status():
    """
    Get comprehensive system health status
    
    Returns detailed health information including:
    - Overall system status
    - Resource utilization
    - Application status
    - Database connectivity
    - Performance metrics summary
    """
    health_data = await health_check_detailed()
    return HealthCheckResponse(**health_data)


@router.get("/health/simple")
async def get_simple_health():
    """
    Simple health check endpoint for load balancers
    
    Returns minimal health status for quick checks
    """
    try:
        health_data = await health_check_detailed()
        return {
            "status": health_data["status"],
            "timestamp": health_data["timestamp"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/metrics", response_model=MetricsSummaryResponse)
async def get_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive metrics summary
    
    Requires authentication. Returns:
    - Performance metrics
    - System resource usage
    - Endpoint statistics
    - Error rates and response times
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    metrics_data = await get_metrics_summary()
    return MetricsSummaryResponse(**metrics_data)


@router.get("/metrics/real-time", response_model=RealTimeMetricsResponse)
async def get_real_time_metrics_endpoint(
    current_user: User = Depends(get_current_user),
    metric_name: Optional[str] = Query(None, description="Specific metric name to retrieve"),
    minutes: int = Query(60, ge=1, le=1440, description="Time window in minutes (max 24 hours)")
):
    """
    Get real-time metrics for specified time window
    
    Requires admin role. Returns time-series data for:
    - System metrics (CPU, memory, disk)
    - Application metrics (requests, errors, response times)
    - Business metrics (AI usage, authentication events)
    """
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    metrics_data = await get_real_time_metrics(metric_name, minutes)
    return RealTimeMetricsResponse(**metrics_data)


@router.get("/metrics/system")
async def get_system_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Get current system resource metrics
    
    Returns real-time system resource utilization
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    import psutil
    import os
    
    # Get current system stats
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = psutil.boot_time()
    uptime = datetime.utcnow().timestamp() - boot_time
    
    # Network connections (simplified)
    connections = len(psutil.net_connections())
    
    system_stats = {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_percent": (disk.used / disk.total) * 100,
        "memory_used_gb": memory.used / (1024**3),
        "memory_total_gb": memory.total / (1024**3),
        "disk_used_gb": disk.used / (1024**3),
        "disk_total_gb": disk.total / (1024**3),
        "load_average": list(os.getloadavg()) if hasattr(os, 'getloadavg') else None,
        "uptime_seconds": uptime,
        "active_connections": connections
    }
    
    return system_stats


@router.get("/metrics/performance")
async def get_performance_metrics(
    current_user: User = Depends(get_current_user),
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze (max 1 week)")
):
    """
    Get application performance metrics
    
    Returns performance analytics including:
    - Request volume and patterns
    - Response time statistics
    - Error rates and types
    - Endpoint performance breakdown
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    # Get metrics for specified time window
    metrics_data = await get_real_time_metrics(None, hours * 60)
    stats = metrics_collector.get_statistics()
    
    # Calculate performance insights
    performance_data = {
        "time_window_hours": hours,
        "summary": {
            "total_requests": stats['request_count'],
            "avg_response_time_ms": stats['avg_response_time'],
            "error_rate": stats['error_rate'],
            "slow_request_rate": stats['slow_request_rate'],
            "requests_per_hour": stats['request_count'] / max(hours, 1)
        },
        "endpoints": stats['endpoint_stats'],
        "status_codes": stats['status_code_stats'],
        "top_errors": [
            {"endpoint": endpoint, "error_count": data["error_count"], "error_rate": data["error_rate"]}
            for endpoint, data in stats['endpoint_stats'].items()
            if data["error_count"] > 0
        ][:10],
        "slowest_endpoints": [
            {"endpoint": endpoint, "avg_time": data["avg_time"], "max_time": data["max_time"]}
            for endpoint, data in stats['endpoint_stats'].items()
        ][:10]
    }
    
    return performance_data


@router.get("/metrics/business")
async def get_business_metrics(
    current_user: User = Depends(get_current_user),
    days: int = Query(7, ge=1, le=30, description="Days to analyze (max 30 days)")
):
    """
    Get business-specific metrics
    
    Returns metrics relevant to business operations:
    - AI service usage
    - Authentication patterns
    - User activity patterns
    - Revenue-impacting metrics
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    # Get business metrics from collector
    ai_metrics = metrics_collector.get_metrics("ai_requests_successful")
    auth_metrics_success = metrics_collector.get_metrics("auth_requests_successful")
    auth_metrics_failed = metrics_collector.get_metrics("auth_requests_failed")
    
    # Calculate business insights
    business_data = {
        "time_window_days": days,
        "ai_service": {
            "total_requests": len(ai_metrics.get("ai_requests_successful", [])),
            "avg_daily_requests": len(ai_metrics.get("ai_requests_successful", [])) / max(days, 1)
        },
        "authentication": {
            "successful_logins": len(auth_metrics_success.get("auth_requests_successful", [])),
            "failed_logins": len(auth_metrics_failed.get("auth_requests_failed", [])),
            "success_rate": 0  # Would calculate based on actual data
        },
        "usage_patterns": {
            "peak_hours": [],  # Would analyze request patterns
            "user_activity": "normal"  # Would calculate based on user sessions
        }
    }
    
    # Calculate authentication success rate
    total_auth = business_data["authentication"]["successful_logins"] + business_data["authentication"]["failed_logins"]
    if total_auth > 0:
        business_data["authentication"]["success_rate"] = round(
            (business_data["authentication"]["successful_logins"] / total_auth) * 100, 2
        )
    
    return business_data


@router.get("/metrics/alerts")
async def get_active_alerts(
    current_user: User = Depends(get_current_user)
):
    """
    Get active system alerts and warnings
    
    Returns current alerts based on thresholds:
    - Performance alerts
    - Resource alerts
    - Error rate alerts
    - Security alerts
    """
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    alerts = []
    stats = metrics_collector.get_statistics()
    
    # Check error rate
    if stats['error_rate'] > 5.0:
        alerts.append({
            "type": "error_rate",
            "severity": "high" if stats['error_rate'] > 10.0 else "medium",
            "message": f"High error rate: {stats['error_rate']}%",
            "value": stats['error_rate'],
            "threshold": 5.0,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    # Check slow request rate
    if stats['slow_request_rate'] > 10.0:
        alerts.append({
            "type": "slow_requests",
            "severity": "medium",
            "message": f"High slow request rate: {stats['slow_request_rate']}%",
            "value": stats['slow_request_rate'],
            "threshold": 10.0,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    # Check system resources
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > 80:
            alerts.append({
                "type": "cpu_usage",
                "severity": "high",
                "message": f"High CPU usage: {cpu_percent}%",
                "value": cpu_percent,
                "threshold": 80.0,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        if memory_percent > 80:
            alerts.append({
                "type": "memory_usage",
                "severity": "high",
                "message": f"High memory usage: {memory_percent}%",
                "value": memory_percent,
                "threshold": 80.0,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    except Exception as e:
        alerts.append({
            "type": "monitoring_error",
            "severity": "low",
            "message": f"Failed to check system resources: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return {
        "active_alerts": alerts,
        "alert_count": len(alerts),
        "highest_severity": max([alert.get("severity", "low") for alert in alerts], default="none"),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/logs/recent")
async def get_recent_logs(
    current_user: User = Depends(get_current_user),
    limit: int = Query(50, le=200, description="Maximum number of logs to return"),
    level: Optional[str] = Query(None, description="Filter by log level (info, warning, error)"),
    category: Optional[str] = Query(None, description="Filter by category (performance, security, error)")
):
    """
    Get recent application logs
    
    Returns recent log entries with filtering options
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    # Get recent requests as log-like data
    recent_requests = list(metrics_collector.recent_requests)[-limit:]
    
    # Filter by category if specified
    if category:
        if category == "error":
            recent_requests = [req for req in recent_requests if req.get("status_code", 200) >= 400]
        elif category == "performance":
            recent_requests = [req for req in recent_requests if req.get("processing_time", 0) > 1000]  # > 1 second
    
    # Format as log entries
    log_entries = []
    for req in recent_requests:
        log_level = "error" if req.get("status_code", 200) >= 400 else "info"
        if level and log_level != level:
            continue
        
        log_entries.append({
            "timestamp": req.get("timestamp"),
            "level": log_level,
            "category": req.get("category", "request"),
            "message": f"{req.get('method', 'GET')} {req.get('path', '/')} - {req.get('status_code', 200)} ({req.get('processing_time', 0)}ms)",
            "details": req
        })
    
    return {
        "logs": log_entries,
        "total_count": len(log_entries),
        "filters": {
            "level": level,
            "category": category,
            "limit": limit
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/metrics/custom")
async def record_custom_metric(
    metric_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Record a custom business metric
    
    Allows applications to record custom metrics for monitoring
    """
    if current_user.user_role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or developer role required."
        )
    
    required_fields = ["name", "value", "type"]
    if not all(field in metric_data for field in required_fields):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {required_fields}"
        )
    
    metric_name = metric_data["name"]
    metric_value = float(metric_data["value"])
    metric_type = metric_data["type"]
    labels = metric_data.get("labels", {})
    
    # Validate metric type
    if metric_type not in ["counter", "gauge", "histogram"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Metric type must be one of: counter, gauge, histogram"
        )
    
    # Record the metric
    try:
        if metric_type == "counter":
            metrics_collector.record_counter(metric_name, metric_value, labels)
        elif metric_type == "gauge":
            metrics_collector.record_gauge(metric_name, metric_value, labels)
        elif metric_type == "histogram":
            metrics_collector.record_histogram(metric_name, metric_value, labels)
        
        return {
            "status": "success",
            "message": f"Custom metric '{metric_name}' recorded successfully",
            "metric": {
                "name": metric_name,
                "value": metric_value,
                "type": metric_type,
                "labels": labels
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record metric: {str(e)}"
        )
