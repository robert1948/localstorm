"""
Error Tracking API Routes for Task 1.3.3 - Comprehensive Error Logs
===================================================================

API endpoints for accessing comprehensive error tracking data:
- Error statistics and trends
- Error details and filtering
- Error pattern analysis
- Real-time error monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.error_tracker import (
    get_error_tracker,
    ErrorSeverity,
    ErrorCategory,
    error_tracker
)
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/errors", tags=["error-tracking"])


@router.get("/statistics")
async def get_error_statistics(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get comprehensive error statistics

    Returns:
        - Total error counts
        - Error rates by time window
        - Errors by severity and category
        - Top error endpoints
        - Recent errors summary
        - Error patterns analysis
    """
    try:
        statistics = error_tracker.get_error_statistics()
        return {
            "status": "success",
            "data": statistics
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error statistics: {str(e)}"
        )


@router.get("/details/{error_id}")
async def get_error_details(
    error_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed information for a specific error

    Args:
        error_id: Unique error identifier

    Returns:
        Comprehensive error context and details
    """
    try:
        error_details = error_tracker.get_error_details(error_id)

        if not error_details:
            raise HTTPException(
                status_code=404,
                detail=f"Error with ID {error_id} not found"
            )

        return {
            "status": "success",
            "data": error_details
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error details: {str(e)}"
        )


@router.get("/by-category/{category}")
async def get_errors_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get errors filtered by category

    Args:
        category: Error category (authentication, database, etc.)
        limit: Maximum number of errors to return

    Returns:
        List of errors in the specified category
    """
    try:
        # Validate category
        try:
            error_category = ErrorCategory(category)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {category}. Valid categories: {[c.value for c in ErrorCategory]}"
            )

        errors = error_tracker.get_errors_by_category(error_category, limit)

        return {
            "status": "success",
            "data": {
                "category": category,
                "total_errors": len(errors),
                "errors": errors
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve errors by category: {str(e)}"
        )


@router.get("/by-severity/{severity}")
async def get_errors_by_severity(
    severity: str,
    limit: int = Query(50, ge=1, le=500),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get errors filtered by severity level

    Args:
        severity: Error severity (low, medium, high, critical)
        limit: Maximum number of errors to return

    Returns:
        List of errors with the specified severity
    """
    try:
        # Validate severity
        try:
            error_severity = ErrorSeverity(severity)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid severity: {severity}. Valid severities: {[s.value for s in ErrorSeverity]}"
            )

        errors = error_tracker.get_errors_by_severity(error_severity, limit)

        return {
            "status": "success",
            "data": {
                "severity": severity,
                "total_errors": len(errors),
                "errors": errors
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve errors by severity: {str(e)}"
        )


@router.get("/trends")
async def get_error_trends(
    hours: int = Query(24, ge=1, le=168),  # Max 1 week
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get error trends over specified time period

    Args:
        hours: Number of hours to analyze (1-168)

    Returns:
        Error trends and patterns over time
    """
    try:
        trends = error_tracker.get_error_trends(hours)

        return {
            "status": "success",
            "data": trends
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error trends: {str(e)}"
        )


@router.get("/real-time")
async def get_real_time_errors(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get real-time error stream (most recent errors)

    Args:
        limit: Maximum number of recent errors to return

    Returns:
        Most recent errors with real-time context
    """
    try:
        with error_tracker._lock:
            recent_errors = list(error_tracker.recent_errors)[-limit:]
            recent_errors.reverse()  # Most recent first

        error_data = [error.to_dict() for error in recent_errors]

        return {
            "status": "success",
            "data": {
                "timestamp": datetime.utcnow().isoformat(),
                "total_recent_errors": len(error_data),
                "errors": error_data
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve real-time errors: {str(e)}"
        )


@router.get("/patterns")
async def get_error_patterns(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get error pattern analysis

    Returns:
        Analysis of recurring error patterns and trends
    """
    try:
        with error_tracker._lock:
            patterns = []

            for signature, pattern in error_tracker.error_patterns.items():
                patterns.append({
                    "pattern_id": pattern.pattern_id,
                    "error_signature": pattern.error_signature,
                    "occurrences": pattern.occurrences,
                    "first_seen": pattern.first_seen.isoformat(),
                    "last_seen": pattern.last_seen.isoformat(),
                    "severity": pattern.severity.value,
                    "category": pattern.category.value,
                    "affected_endpoints": pattern.affected_endpoints,
                    "affected_users_count": len(pattern.affected_users),
                    "frequency_per_hour": round(
                        pattern.occurrences / max(
                            (pattern.last_seen - pattern.first_seen).total_seconds() / 3600,
                            1
                        ), 2
                    )
                })

        # Sort by occurrences (most frequent first)
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)

        return {
            "status": "success",
            "data": {
                "timestamp": datetime.utcnow().isoformat(),
                "total_patterns": len(patterns),
                "patterns": patterns
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error patterns: {str(e)}"
        )


@router.get("/summary")
async def get_error_summary(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get high-level error summary for dashboards

    Returns:
        Concise error summary with key metrics
    """
    try:
        statistics = error_tracker.get_error_statistics()

        # Calculate error rate trends
        current_time = datetime.utcnow()
        last_hour_errors = 0
        last_24h_errors = 0

        with error_tracker._lock:
            for error in error_tracker.recent_errors:
                if error.timestamp >= current_time - timedelta(hours=1):
                    last_hour_errors += 1
                if error.timestamp >= current_time - timedelta(hours=24):
                    last_24h_errors += 1

        # Calculate critical error percentage
        total_errors = statistics["total_errors"]
        critical_errors = statistics["errors_by_severity"].get("critical", 0)
        high_errors = statistics["errors_by_severity"].get("high", 0)

        critical_percentage = (
            (critical_errors + high_errors) / max(total_errors, 1) * 100
        )

        # Get top error category
        top_category = max(
            statistics["errors_by_category"].items(),
            key=lambda x: x[1]
        ) if statistics["errors_by_category"] else ("unknown", 0)

        return {
            "status": "success",
            "data": {
                "timestamp": current_time.isoformat(),
                "total_errors": total_errors,
                "last_hour_errors": last_hour_errors,
                "last_24h_errors": last_24h_errors,
                "critical_error_percentage": round(critical_percentage, 1),
                "top_error_category": {
                    "category": top_category[0],
                    "count": top_category[1]
                },
                "error_rate_1min": statistics["error_rates"]["1min"],
                "error_rate_5min": statistics["error_rates"]["5min"],
                "error_rate_1hour": statistics["error_rates"]["1hour"],
                "active_patterns": len(statistics["error_patterns"]),
                "health_status": _calculate_error_health_status(
                    last_hour_errors, critical_percentage
                )
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error summary: {str(e)}"
        )


def _calculate_error_health_status(hourly_errors: int, critical_percentage: float) -> str:
    """Calculate system health based on error metrics"""
    if critical_percentage > 10 or hourly_errors > 100:
        return "critical"
    elif critical_percentage > 5 or hourly_errors > 50:
        return "degraded"
    elif critical_percentage > 2 or hourly_errors > 20:
        return "warning"
    else:
        return "healthy"


@router.post("/track")
async def track_manual_error(
    error_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Track a manual error.

    Args:
        error_data: Error information to track

    Returns:
        Error tracking confirmation with error ID
    """
    try:
        # Extract error information
        error_message = error_data.get("error_message", "Manual error")
        severity = ErrorSeverity(error_data.get("severity", "medium"))
        category = ErrorCategory(error_data.get("category", "unknown"))

        # Track the error
        error_id = error_tracker.track_error(
            error_message=error_message,
            severity=severity,
            category=category,
            endpoint=error_data.get("endpoint"),
            user_id=str(current_user.id),
            additional_context=error_data.get("additional_context", {})
        )

        return {
            "status": "success",
            "data": {
                "error_id": error_id,
                "message": "Error tracked successfully"
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid error data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to track error: {str(e)}"
        )


@router.get("/health")
async def get_error_tracking_health() -> Dict[str, Any]:
    """
    Get error tracking system health status

    Returns:
        Health status of the error tracking system
    """
    try:
        statistics = error_tracker.get_error_statistics()

        # Calculate health metrics
        total_errors = statistics["total_errors"]
        recent_errors = len(statistics["recent_errors"])
        patterns_count = statistics["patterns_count"]

        # Determine health status
        if total_errors > 50000 or recent_errors > 1000:
            health_status = "overloaded"
        elif total_errors > 10000 or recent_errors > 500:
            health_status = "high_load"
        elif total_errors > 1000 or recent_errors > 100:
            health_status = "moderate_load"
        else:
            health_status = "healthy"

        return {
            "status": "success",
            "data": {
                "timestamp": datetime.utcnow().isoformat(),
                "health_status": health_status,
                "total_errors_tracked": total_errors,
                "recent_errors_count": recent_errors,
                "active_patterns": patterns_count,
                "system_capacity": {
                    "max_errors": error_tracker.max_errors,
                    "max_patterns": error_tracker.max_patterns,
                    "current_usage_percentage": round(
                        (recent_errors / error_tracker.max_errors) * 100, 1
                    )
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve error tracking health: {str(e)}"
        )
