"""
Error Tracking Enhancement for Task 1.3.3 - Comprehensive Error Logs
====================================================================

Advanced error tracking service that provides:
- Comprehensive error categorization and analysis
- Real-time error aggregation and trends
- Advanced error context capture
- Error-based alerting and notifications
- Integration with monitoring and audit systems
"""

import logging
import traceback
import threading
import hashlib
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.audit_service import get_audit_logger, AuditEventType, AuditLogLevel


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    SYSTEM = "system"
    BUSINESS_LOGIC = "business_logic"
    NETWORK = "network"
    PERFORMANCE = "performance"
    SECURITY = "security"
    AI_SERVICE = "ai_service"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Comprehensive error context information"""
    timestamp: datetime
    error_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    stack_trace: Optional[str]
    user_id: Optional[str]
    session_id: Optional[str]
    endpoint: Optional[str]
    http_method: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]
    request_data: Optional[Dict[str, Any]]
    response_status: Optional[int]
    processing_time_ms: Optional[float]
    additional_context: Optional[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "error_id": self.error_id,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "severity": self.severity.value,
            "category": self.category.value,
            "stack_trace": self.stack_trace,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "endpoint": self.endpoint,
            "http_method": self.http_method,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "request_data": self.request_data,
            "response_status": self.response_status,
            "processing_time_ms": self.processing_time_ms,
            "additional_context": self.additional_context
        }


@dataclass
class ErrorPattern:
    """Error pattern for trend analysis"""
    pattern_id: str
    error_signature: str
    occurrences: int
    first_seen: datetime
    last_seen: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    affected_endpoints: List[str]
    affected_users: List[str]


class ErrorTracker:
    """
    Advanced error tracking system with comprehensive analysis
    """
    
    def __init__(self, max_errors: int = 10000, max_patterns: int = 1000):
        self.max_errors = max_errors
        self.max_patterns = max_patterns
        
        # Thread-safe storage
        self._lock = threading.Lock()
        
        # Error storage
        self.recent_errors: deque = deque(maxlen=max_errors)
        self.error_patterns: Dict[str, ErrorPattern] = {}
        
        # Statistics
        self.total_errors = 0
        self.errors_by_severity = defaultdict(int)
        self.errors_by_category = defaultdict(int)
        self.errors_by_endpoint = defaultdict(int)
        self.errors_by_hour = defaultdict(int)
        
        # Rate tracking
        self.error_rates = {
            "1min": deque(maxlen=60),
            "5min": deque(maxlen=300),
            "1hour": deque(maxlen=3600)
        }
        
        # Setup logging
        self.setup_logging()
        self.audit_logger = get_audit_logger()
        
        # Start background processing
        self._start_background_processing()
    
    def setup_logging(self):
        """Setup specialized error tracking loggers"""
        # Main error tracking logger
        self.logger = logging.getLogger("localstorm.error_tracker")
        self.logger.setLevel(logging.INFO)
        
        # Specialized loggers
        self.critical_logger = logging.getLogger("localstorm.critical_errors")
        self.security_logger = logging.getLogger("localstorm.security_errors")
        self.performance_logger = logging.getLogger("localstorm.performance_errors")
        self.business_logger = logging.getLogger("localstorm.business_errors")
        
        # Set log levels
        self.critical_logger.setLevel(logging.CRITICAL)
        self.security_logger.setLevel(logging.ERROR)
        self.performance_logger.setLevel(logging.WARNING)
        self.business_logger.setLevel(logging.ERROR)
    
    def _start_background_processing(self):
        """Start background thread for error analysis"""
        def background_processor():
            while True:
                try:
                    self._analyze_error_trends()
                    self._cleanup_old_data()
                    time.sleep(60)  # Run every minute
                except Exception as e:
                    self.logger.error(f"Error in background processing: {str(e)}")
        
        thread = threading.Thread(target=background_processor, daemon=True)
        thread.start()
    
    def track_error(self, 
                   exception: Optional[Exception] = None,
                   error_message: Optional[str] = None,
                   severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                   category: ErrorCategory = ErrorCategory.UNKNOWN,
                   endpoint: Optional[str] = None,
                   http_method: Optional[str] = None,
                   user_id: Optional[str] = None,
                   session_id: Optional[str] = None,
                   user_agent: Optional[str] = None,
                   ip_address: Optional[str] = None,
                   request_data: Optional[Dict[str, Any]] = None,
                   response_status: Optional[int] = None,
                   processing_time_ms: Optional[float] = None,
                   additional_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Track a comprehensive error with full context
        
        Returns:
            str: Unique error ID for tracking
        """
        
        # Extract error information
        error_type = type(exception).__name__ if exception else "Manual"
        error_msg = str(exception) if exception else error_message or "Unknown error"
        stack_trace = traceback.format_exc() if exception else None
        
        # Generate unique error ID
        error_signature = f"{error_type}:{error_msg}:{endpoint or 'unknown'}"
        error_id = hashlib.md5(f"{error_signature}:{datetime.utcnow().isoformat()}".encode()).hexdigest()
        
        # Create error context
        error_context = ErrorContext(
            timestamp=datetime.utcnow(),
            error_id=error_id,
            error_type=error_type,
            error_message=error_msg,
            severity=severity,
            category=category,
            stack_trace=stack_trace,
            user_id=user_id,
            session_id=session_id,
            endpoint=endpoint,
            http_method=http_method,
            user_agent=user_agent,
            ip_address=ip_address,
            request_data=request_data,
            response_status=response_status,
            processing_time_ms=processing_time_ms,
            additional_context=additional_context
        )
        
        # Thread-safe update
        with self._lock:
            self._update_statistics(error_context)
            self._update_patterns(error_context)
            self._store_error(error_context)
        
        # Log error based on severity
        self._log_error(error_context)
        
        # Audit log for critical errors
        if severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            self._audit_log_error(error_context)
        
        return error_id
    
    def _update_statistics(self, error_context: ErrorContext):
        """Update error statistics"""
        self.total_errors += 1
        self.errors_by_severity[error_context.severity.value] += 1
        self.errors_by_category[error_context.category.value] += 1
        
        if error_context.endpoint:
            self.errors_by_endpoint[error_context.endpoint] += 1
        
        # Update hourly statistics
        hour_key = error_context.timestamp.strftime("%Y-%m-%d:%H")
        self.errors_by_hour[hour_key] += 1
        
        # Update rate tracking
        current_time = time.time()
        for rate_window in self.error_rates:
            self.error_rates[rate_window].append(current_time)
    
    def _update_patterns(self, error_context: ErrorContext):
        """Update error pattern analysis"""
        pattern_signature = f"{error_context.error_type}:{error_context.category.value}"
        
        if pattern_signature in self.error_patterns:
            pattern = self.error_patterns[pattern_signature]
            pattern.occurrences += 1
            pattern.last_seen = error_context.timestamp
            
            if error_context.endpoint and error_context.endpoint not in pattern.affected_endpoints:
                pattern.affected_endpoints.append(error_context.endpoint)
            
            if error_context.user_id and error_context.user_id not in pattern.affected_users:
                pattern.affected_users.append(error_context.user_id)
        else:
            # Create new pattern
            if len(self.error_patterns) < self.max_patterns:
                pattern_id = hashlib.md5(pattern_signature.encode()).hexdigest()[:8]
                self.error_patterns[pattern_signature] = ErrorPattern(
                    pattern_id=pattern_id,
                    error_signature=pattern_signature,
                    occurrences=1,
                    first_seen=error_context.timestamp,
                    last_seen=error_context.timestamp,
                    severity=error_context.severity,
                    category=error_context.category,
                    affected_endpoints=[error_context.endpoint] if error_context.endpoint else [],
                    affected_users=[error_context.user_id] if error_context.user_id else []
                )
    
    def _store_error(self, error_context: ErrorContext):
        """Store error in recent errors collection"""
        self.recent_errors.append(error_context)
    
    def _log_error(self, error_context: ErrorContext):
        """Log error based on severity and category"""
        error_data = error_context.to_dict()
        log_message = f"ERROR_TRACKED: {json.dumps(error_data, default=str)}"
        
        # Log to appropriate logger based on severity
        if error_context.severity == ErrorSeverity.CRITICAL:
            self.critical_logger.critical(log_message)
        elif error_context.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif error_context.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
        
        # Log to category-specific loggers
        if error_context.category == ErrorCategory.SECURITY:
            self.security_logger.error(f"SECURITY_ERROR: {log_message}")
        elif error_context.category == ErrorCategory.PERFORMANCE:
            self.performance_logger.warning(f"PERFORMANCE_ERROR: {log_message}")
        elif error_context.category in [ErrorCategory.BUSINESS_LOGIC, ErrorCategory.AI_SERVICE]:
            self.business_logger.error(f"BUSINESS_ERROR: {log_message}")
    
    def _audit_log_error(self, error_context: ErrorContext):
        """Log critical errors to audit system"""
        try:
            db = next(get_db())
            
            # Determine audit event type based on category
            event_type_mapping = {
                ErrorCategory.AUTHENTICATION: AuditEventType.USER_LOGIN_FAILED,
                ErrorCategory.AUTHORIZATION: AuditEventType.UNAUTHORIZED_ACCESS,
                ErrorCategory.SECURITY: AuditEventType.SECURITY_VIOLATION,
                ErrorCategory.DATABASE: AuditEventType.DATA_ACCESS,
                ErrorCategory.AI_SERVICE: AuditEventType.AI_REQUEST_PROCESSED
            }
            
            event_type = event_type_mapping.get(error_context.category, AuditEventType.SYSTEM_ERROR)
            
            self.audit_logger.log_event(
                db=db,
                event_type=event_type,
                event_level=AuditLogLevel.ERROR,
                user_id=error_context.user_id,
                user_email=None,
                user_role=None,
                ip_address=error_context.ip_address,
                user_agent=error_context.user_agent,
                endpoint=error_context.endpoint,
                http_method=error_context.http_method,
                success=False,
                error_message=error_context.error_message,
                metadata={
                    "error_id": error_context.error_id,
                    "error_type": error_context.error_type,
                    "severity": error_context.severity.value,
                    "category": error_context.category.value,
                    "processing_time_ms": error_context.processing_time_ms,
                    "additional_context": error_context.additional_context
                }
            )
            
            db.close()
        except Exception as e:
            self.logger.error(f"Failed to audit log error: {str(e)}")
    
    def _analyze_error_trends(self):
        """Analyze error trends and patterns"""
        try:
            with self._lock:
                # Clean up old rate data
                current_time = time.time()
                for window, rate_data in self.error_rates.items():
                    if window == "1min":
                        cutoff = current_time - 60
                    elif window == "5min":
                        cutoff = current_time - 300
                    else:  # 1hour
                        cutoff = current_time - 3600
                    
                    # Remove old entries
                    while rate_data and rate_data[0] < cutoff:
                        rate_data.popleft()
                
                # Identify trending errors
                trending_patterns = []
                for signature, pattern in self.error_patterns.items():
                    if pattern.occurrences > 10 and pattern.last_seen > datetime.utcnow() - timedelta(hours=1):
                        trending_patterns.append(pattern)
                
                # Log trending errors
                if trending_patterns:
                    self.logger.warning(
                        f"TRENDING_ERRORS: {len(trending_patterns)} error patterns trending in last hour"
                    )
                    
                    for pattern in trending_patterns[:5]:  # Top 5
                        self.logger.warning(
                            f"TRENDING_PATTERN: {pattern.error_signature} "
                            f"- {pattern.occurrences} occurrences, "
                            f"affecting {len(pattern.affected_endpoints)} endpoints"
                        )
        
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {str(e)}")
    
    def _cleanup_old_data(self):
        """Clean up old error data"""
        try:
            with self._lock:
                # Clean up old hourly statistics (keep last 7 days)
                cutoff_time = datetime.utcnow() - timedelta(days=7)
                cutoff_hour = cutoff_time.strftime("%Y-%m-%d:%H")
                
                old_hours = [
                    hour for hour in self.errors_by_hour.keys()
                    if hour < cutoff_hour
                ]
                
                for hour in old_hours:
                    del self.errors_by_hour[hour]
                
                # Clean up old patterns (keep active ones)
                old_patterns = [
                    signature for signature, pattern in self.error_patterns.items()
                    if pattern.last_seen < cutoff_time
                ]
                
                for signature in old_patterns:
                    del self.error_patterns[signature]
        
        except Exception as e:
            self.logger.error(f"Error in cleanup: {str(e)}")
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get comprehensive error statistics"""
        with self._lock:
            current_time = time.time()
            
            # Calculate error rates
            error_rates = {}
            for window, rate_data in self.error_rates.items():
                error_rates[window] = len(rate_data)
            
            # Recent errors summary
            recent_errors_summary = []
            for error in list(self.recent_errors)[-10:]:  # Last 10 errors
                recent_errors_summary.append({
                    "timestamp": error.timestamp.isoformat(),
                    "error_id": error.error_id,
                    "error_type": error.error_type,
                    "severity": error.severity.value,
                    "category": error.category.value,
                    "endpoint": error.endpoint
                })
            
            # Top error patterns
            top_patterns = sorted(
                self.error_patterns.values(),
                key=lambda p: p.occurrences,
                reverse=True
            )[:10]
            
            pattern_summary = []
            for pattern in top_patterns:
                pattern_summary.append({
                    "pattern_id": pattern.pattern_id,
                    "error_signature": pattern.error_signature,
                    "occurrences": pattern.occurrences,
                    "first_seen": pattern.first_seen.isoformat(),
                    "last_seen": pattern.last_seen.isoformat(),
                    "severity": pattern.severity.value,
                    "category": pattern.category.value,
                    "affected_endpoints": len(pattern.affected_endpoints),
                    "affected_users": len(pattern.affected_users)
                })
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "total_errors": self.total_errors,
                "error_rates": error_rates,
                "errors_by_severity": dict(self.errors_by_severity),
                "errors_by_category": dict(self.errors_by_category),
                "top_error_endpoints": dict(sorted(
                    self.errors_by_endpoint.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]),
                "recent_errors": recent_errors_summary,
                "error_patterns": pattern_summary,
                "patterns_count": len(self.error_patterns)
            }
    
    def get_error_details(self, error_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific error"""
        with self._lock:
            for error in self.recent_errors:
                if error.error_id == error_id:
                    return error.to_dict()
        return None
    
    def get_errors_by_category(self, category: ErrorCategory, limit: int = 50) -> List[Dict[str, Any]]:
        """Get errors filtered by category"""
        with self._lock:
            category_errors = [
                error.to_dict() for error in self.recent_errors
                if error.category == category
            ]
            return sorted(category_errors, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_errors_by_severity(self, severity: ErrorSeverity, limit: int = 50) -> List[Dict[str, Any]]:
        """Get errors filtered by severity"""
        with self._lock:
            severity_errors = [
                error.to_dict() for error in self.recent_errors
                if error.severity == severity
            ]
            return sorted(severity_errors, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_error_trends(self, hours: int = 24) -> Dict[str, Any]:
        """Get error trends for specified time period"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        with self._lock:
            # Filter recent errors by time
            recent_errors = [
                error for error in self.recent_errors
                if error.timestamp >= cutoff_time
            ]
            
            # Group by hour
            hourly_counts = defaultdict(int)
            hourly_severity = defaultdict(lambda: defaultdict(int))
            hourly_category = defaultdict(lambda: defaultdict(int))
            
            for error in recent_errors:
                hour_key = error.timestamp.strftime("%Y-%m-%d:%H")
                hourly_counts[hour_key] += 1
                hourly_severity[hour_key][error.severity.value] += 1
                hourly_category[hour_key][error.category.value] += 1
            
            return {
                "time_period_hours": hours,
                "total_errors": len(recent_errors),
                "hourly_counts": dict(hourly_counts),
                "hourly_severity": {k: dict(v) for k, v in hourly_severity.items()},
                "hourly_category": {k: dict(v) for k, v in hourly_category.items()}
            }


# Global error tracker instance
error_tracker = ErrorTracker()


def track_error(**kwargs) -> str:
    """Convenience function to track errors"""
    return error_tracker.track_error(**kwargs)


def get_error_tracker() -> ErrorTracker:
    """Get the global error tracker instance"""
    return error_tracker
