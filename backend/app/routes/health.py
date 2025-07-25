"""
Enhanced Health Check API Routes for Task 1.3.5 - Advanced Endpoint Monitoring
================================================================================

Comprehensive health check API providing:
- Advanced health monitoring endpoints
- Service-specific health checks
- Historical health data and trends
- Real-time health status streaming
- Custom health check registration
- Health alerting and notifications
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime, timedelta

from app.services.health_service import get_health_service, HealthService, EndpointHealthCheck
from app.middleware.auth import verify_token_optional, verify_admin_token
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/health", tags=["Health Monitoring"])


@router.get("/status")
async def get_health_status():
    """
    Quick health status check
    Returns basic system health information
    """
    health_service = get_health_service()
    return await health_service.run_comprehensive_health_check()


@router.get("/detailed")
async def get_detailed_health_check():
    """
    Comprehensive detailed health check
    Returns full health assessment with trends and suggestions
    """
    health_service = get_health_service()
    return await health_service.run_comprehensive_health_check()


@router.get("/services")
async def list_health_services():
    """
    List all registered health services
    """
    health_service = get_health_service()
    return health_service.get_health_summary()


@router.get("/services/{service_name}")
async def get_service_health(service_name: str):
    """
    Get health status for a specific service
    """
    health_service = get_health_service()
    result = await health_service.get_service_health(service_name)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/endpoints")
async def get_endpoint_health():
    """
    Get health status for all monitored endpoints
    """
    health_service = get_health_service()
    comprehensive_check = await health_service.run_comprehensive_health_check()
    
    return {
        "endpoints": comprehensive_check.get("endpoints", {}),
        "timestamp": comprehensive_check.get("timestamp"),
        "check_duration_ms": comprehensive_check.get("check_duration_ms")
    }


@router.get("/metrics")
async def get_health_metrics():
    """
    Get system health metrics
    """
    health_service = get_health_service()
    comprehensive_check = await health_service.run_comprehensive_health_check()
    
    return {
        "system_metrics": comprehensive_check.get("system_metrics", {}),
        "overall_status": comprehensive_check.get("overall_status"),
        "timestamp": comprehensive_check.get("timestamp")
    }


@router.get("/trends")
async def get_health_trends(
    service: Optional[str] = Query(None, description="Filter by specific service"),
    hours: int = Query(24, description="Hours of history to analyze")
):
    """
    Get health trends and historical data
    """
    health_service = get_health_service()
    comprehensive_check = await health_service.run_comprehensive_health_check()
    
    trends = comprehensive_check.get("trends", {})
    
    if service:
        if service not in trends:
            raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
        return {"service": service, "trend": trends[service]}
    
    return {"trends": trends, "analysis_period_hours": hours}


@router.get("/alerts")
async def get_health_alerts():
    """
    Get current health alerts and issues
    """
    health_service = get_health_service()
    comprehensive_check = await health_service.run_comprehensive_health_check()
    
    return {
        "alerts": comprehensive_check.get("alerts", []),
        "suggestions": comprehensive_check.get("suggestions", []),
        "overall_status": comprehensive_check.get("overall_status"),
        "timestamp": comprehensive_check.get("timestamp")
    }


@router.get("/stream")
async def stream_health_status():
    """
    Stream real-time health status updates
    Server-sent events endpoint for live health monitoring
    """
    async def generate_health_stream():
        health_service = get_health_service()
        
        while True:
            try:
                # Get current health status
                health_data = await health_service.run_comprehensive_health_check()
                
                # Format as server-sent event
                yield f"data: {json.dumps(health_data)}\n\n"
                
                # Wait before next update
                await asyncio.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                error_data = {
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                await asyncio.sleep(30)
    
    return StreamingResponse(
        generate_health_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )


@router.post("/endpoints/register")
async def register_endpoint_check(
    endpoint_data: Dict[str, Any],
    _: dict = Depends(verify_admin_token)
):
    """
    Register a new endpoint for health monitoring
    Requires admin authentication
    """
    try:
        endpoint_check = EndpointHealthCheck(**endpoint_data)
        health_service = get_health_service()
        health_service.register_endpoint_check(endpoint_check)
        
        return {
            "message": f"Endpoint '{endpoint_check.name}' registered successfully",
            "endpoint": endpoint_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid endpoint configuration: {str(e)}")


@router.delete("/endpoints/{endpoint_name}")
async def unregister_endpoint_check(
    endpoint_name: str,
    _: dict = Depends(verify_admin_token)
):
    """
    Unregister an endpoint from health monitoring
    Requires admin authentication
    """
    health_service = get_health_service()
    
    # Find and remove the endpoint
    initial_count = len(health_service.endpoint_checks)
    health_service.endpoint_checks = [
        ep for ep in health_service.endpoint_checks 
        if ep.name != endpoint_name
    ]
    
    if len(health_service.endpoint_checks) == initial_count:
        raise HTTPException(status_code=404, detail=f"Endpoint '{endpoint_name}' not found")
    
    return {"message": f"Endpoint '{endpoint_name}' unregistered successfully"}


@router.get("/database")
async def check_database_health():
    """
    Specific database health check
    """
    health_service = get_health_service()
    result = await health_service.get_service_health("database_connection")
    
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    
    return result


@router.get("/system")
async def check_system_health():
    """
    Specific system resources health check
    """
    health_service = get_health_service()
    result = await health_service.get_service_health("system_resources")
    
    return result


@router.get("/errors")
async def check_error_health():
    """
    Specific error rates health check
    """
    health_service = get_health_service()
    result = await health_service.get_service_health("error_rates")
    
    return result


@router.get("/disk")
async def check_disk_health():
    """
    Specific disk space health check
    """
    health_service = get_health_service()
    result = await health_service.get_service_health("disk_space")
    
    return result


@router.get("/process")
async def check_process_health():
    """
    Specific process health check
    """
    health_service = get_health_service()
    result = await health_service.get_service_health("process_health")
    
    return result


@router.post("/check")
async def trigger_health_check(
    background_tasks: BackgroundTasks,
    services: Optional[List[str]] = None
):
    """
    Trigger an immediate health check
    Optionally specify which services to check
    """
    async def run_background_check():
        health_service = get_health_service()
        
        if services:
            # Run specific service checks
            results = {}
            for service_name in services:
                if service_name in health_service.health_checks:
                    result = await health_service.get_service_health(service_name)
                    results[service_name] = result
            return results
        else:
            # Run comprehensive check
            return await health_service.run_comprehensive_health_check()
    
    # Start background check
    background_tasks.add_task(run_background_check)
    
    return {
        "message": "Health check triggered",
        "services": services if services else "all",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/config")
async def get_health_config():
    """
    Get current health check configuration
    """
    health_service = get_health_service()
    
    return {
        "thresholds": health_service.thresholds,
        "registered_checks": list(health_service.health_checks.keys()),
        "registered_endpoints": [
            {
                "name": ep.name,
                "url": ep.url,
                "method": ep.method,
                "critical": ep.critical,
                "timeout": ep.timeout
            }
            for ep in health_service.endpoint_checks
        ]
    }


@router.put("/config/thresholds")
async def update_health_thresholds(
    thresholds: Dict[str, float],
    _: dict = Depends(verify_admin_token)
):
    """
    Update health check thresholds
    Requires admin authentication
    """
    health_service = get_health_service()
    
    # Validate threshold keys
    valid_keys = set(health_service.thresholds.keys())
    provided_keys = set(thresholds.keys())
    
    invalid_keys = provided_keys - valid_keys
    if invalid_keys:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid threshold keys: {list(invalid_keys)}. Valid keys: {list(valid_keys)}"
        )
    
    # Update thresholds
    health_service.thresholds.update(thresholds)
    
    return {
        "message": "Health thresholds updated successfully",
        "updated_thresholds": thresholds,
        "current_thresholds": health_service.thresholds
    }


@router.get("/history/{service_name}")
async def get_service_health_history(
    service_name: str,
    limit: int = Query(50, description="Number of historical records to return")
):
    """
    Get historical health data for a specific service
    """
    health_service = get_health_service()
    
    if service_name not in health_service.health_checks:
        raise HTTPException(
            status_code=404, 
            detail=f"Service '{service_name}' not found"
        )
    
    history = list(health_service.health_history[service_name])
    
    # Limit results
    if limit > 0:
        history = history[-limit:]
    
    return {
        "service": service_name,
        "history": history,
        "total_records": len(health_service.health_history[service_name]),
        "returned_records": len(history)
    }


@router.get("/summary")
async def get_health_summary():
    """
    Get a comprehensive health summary
    """
    health_service = get_health_service()
    comprehensive_check = await health_service.run_comprehensive_health_check()
    
    # Extract key metrics for summary
    services_status = {}
    for service_name, service_data in comprehensive_check.get("services", {}).items():
        services_status[service_name] = service_data.get("status")
    
    endpoints_status = {}
    for endpoint_name, endpoint_data in comprehensive_check.get("endpoints", {}).items():
        endpoints_status[endpoint_name] = endpoint_data.get("status")
    
    return {
        "overall_status": comprehensive_check.get("overall_status"),
        "services_summary": services_status,
        "endpoints_summary": endpoints_status,
        "active_alerts": len(comprehensive_check.get("alerts", [])),
        "system_health": {
            "cpu_ok": comprehensive_check.get("system_metrics", {}).get("cpu", {}).get("percent", 0) < 80,
            "memory_ok": comprehensive_check.get("system_metrics", {}).get("memory", {}).get("percent", 0) < 80,
            "disk_ok": comprehensive_check.get("system_metrics", {}).get("disk", {}).get("percent", 0) < 80
        },
        "timestamp": comprehensive_check.get("timestamp"),
        "check_duration_ms": comprehensive_check.get("check_duration_ms")
    }
