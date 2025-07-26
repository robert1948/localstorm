"""
Enhanced Monitoring Middleware for Task 1.3.1 - Real-time Metrics Collection
Enhanced for Task 1.3.3 - Comprehensive Error Logs Integration
============================================================================

Comprehensive monitoring middleware that provides:
- Real-time metrics collection and storage
- Performance monitoring and alerting
- System health monitoring
- Request/response analytics
- Enhanced error tracking and aggregation with comprehensive logs
- Custom metrics for business logic
- Integration with advanced error tracking system
"""

import logging
import time
import threading
import os
import psutil
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import json
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.audit_service import get_audit_logger, AuditEventType, AuditLogLevel
from app.services.error_tracker import get_error_tracker, ErrorSeverity, ErrorCategory


@dataclass
class MetricPoint:
    """Data class for metric points"""
    timestamp: datetime
    value: float
    labels: Dict[str, str]
    metric_type: str  # counter, gauge, histogram

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels,
            "metric_type": self.metric_type
        }


class MetricsCollector:
    """Thread-safe metrics collector for real-time metrics"""

    def __init__(self, max_points: int = 10000):
        self.max_points = max_points
        self.metrics = defaultdict(lambda: deque(maxlen=max_points))
        self.counters = defaultdict(float)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self._lock = threading.Lock()

        # Performance statistics
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.slow_request_count = 0

        # Endpoint statistics
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'error_count': 0,
            'min_time': float('inf'),
            'max_time': 0.0
        })

        # Status code statistics
        self.status_code_stats = defaultdict(int)

        # User agent statistics
        self.user_agent_stats = defaultdict(int)

        # Recent requests (for debugging)
        self.recent_requests = deque(maxlen=100)

    def record_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        """Record a counter metric"""
        with self._lock:
            key = f"{name}_{hash(str(labels or {}))}"
            self.counters[key] += value

            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {},
                metric_type="counter"
            )
            self.metrics[name].append(metric_point)

    def record_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a gauge metric"""
        with self._lock:
            key = f"{name}_{hash(str(labels or {}))}"
            self.gauges[key] = value

            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {},
                metric_type="gauge"
            )
            self.metrics[name].append(metric_point)

    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram metric"""
        with self._lock:
            key = f"{name}_{hash(str(labels or {}))}"
            self.histograms[key].append(value)

            # Keep only recent values
            if len(self.histograms[key]) > 1000:
                self.histograms[key] = self.histograms[key][-1000:]

            metric_point = MetricPoint(
                timestamp=datetime.utcnow(),
                value=value,
                labels=labels or {},
                metric_type="histogram"
            )
            self.metrics[name].append(metric_point)

    def get_metrics(self, name: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Get all metrics or specific metric"""
        with self._lock:
            if name:
                return {name: [point.to_dict() for point in self.metrics.get(name, [])]}

            return {
                metric_name: [point.to_dict() for point in points]
                for metric_name, points in self.metrics.items()
            }

    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregated statistics"""
        with self._lock:
            avg_response_time = (
                self.total_response_time / self.request_count
                if self.request_count > 0 else 0
            )

            error_rate = (
                self.error_count / self.request_count * 100
                if self.request_count > 0 else 0
            )

            # Calculate endpoint statistics
            endpoint_summary = {}
            for endpoint, stats in self.endpoint_stats.items():
                if stats['count'] > 0:
                    endpoint_summary[endpoint] = {
                        'count': stats['count'],
                        'avg_time': stats['total_time'] / stats['count'],
                        'error_count': stats['error_count'],
                        'error_rate': stats['error_count'] / stats['count'] * 100,
                        'min_time': stats['min_time'] if stats['min_time'] != float('inf') else 0,
                        'max_time': stats['max_time']
                    }

            return {
                'request_count': self.request_count,
                'error_count': self.error_count,
                'error_rate': round(error_rate, 2),
                'avg_response_time': round(avg_response_time * 1000, 2),  # Convert to ms
                'slow_request_count': self.slow_request_count,
                'slow_request_rate': round(self.slow_request_count / self.request_count * 100, 2) if self.request_count > 0 else 0,
                'endpoint_stats': endpoint_summary,
                'status_code_stats': dict(self.status_code_stats),
                'top_user_agents': dict(list(self.user_agent_stats.items())[:10])
            }


# Global metrics collector instance
metrics_collector = MetricsCollector()


class MonitoringMiddleware(BaseHTTPMiddleware):
    """
    Enhanced middleware for comprehensive monitoring and real-time metrics collection
    Integrated with advanced error tracking system for Task 1.3.3

    Features:
    - Real-time metrics collection
    - Performance monitoring
    - Enhanced error tracking and comprehensive logging
    - System health monitoring
    - Request/response analytics
    - Custom business metrics
    - Integration with error tracking service
    """

    def __init__(self, app, enable_detailed_logging: bool = True, alert_thresholds: Dict[str, Any] = None):
        super().__init__(app)
        self.enable_detailed_logging = enable_detailed_logging
        self.alert_thresholds = alert_thresholds or {
            'slow_request_threshold': 2.0,  # seconds
            'error_rate_threshold': 5.0,    # percentage
            'memory_threshold': 80.0,       # percentage
            'cpu_threshold': 80.0           # percentage
        }
        self.setup_logging()
        self.audit_logger = get_audit_logger()
        self.error_tracker = get_error_tracker()  # Enhanced error tracking

        # Start background monitoring
        self._start_system_monitoring()

    def setup_logging(self):
        """Setup structured logging with different log levels"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Main logger
        self.logger = logging.getLogger("localstorm.monitoring")

        # Specialized loggers
        self.performance_logger = logging.getLogger("localstorm.performance")
        self.security_logger = logging.getLogger("localstorm.security")
        self.error_logger = logging.getLogger("localstorm.errors")
        self.business_logger = logging.getLogger("localstorm.business")
        self.system_logger = logging.getLogger("localstorm.system")

        # Set appropriate log levels
        self.performance_logger.setLevel(logging.INFO)
        self.security_logger.setLevel(logging.WARNING)
        self.error_logger.setLevel(logging.ERROR)
        self.business_logger.setLevel(logging.INFO)
        self.system_logger.setLevel(logging.INFO)

    def _start_system_monitoring(self):
        """Start background system monitoring"""
        def monitor_system():
            while True:
                try:
                    # System metrics
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')

                    # Record system metrics
                    metrics_collector.record_gauge("system_cpu_percent", cpu_percent)
                    metrics_collector.record_gauge("system_memory_percent", memory.percent)
                    metrics_collector.record_gauge("system_disk_percent", disk.percent)
                    metrics_collector.record_gauge("system_memory_available", memory.available)

                    # Check thresholds and alert
                    if cpu_percent > self.alert_thresholds['cpu_threshold']:
                        self.system_logger.warning(f"High CPU usage: {cpu_percent}%")

                    if memory.percent > self.alert_thresholds['memory_threshold']:
                        self.system_logger.warning(f"High memory usage: {memory.percent}%")

                    # Load average (Unix-like systems)
                    if hasattr(os, 'getloadavg'):
                        load_avg = os.getloadavg()
                        metrics_collector.record_gauge("system_load_1m", load_avg[0])
                        metrics_collector.record_gauge("system_load_5m", load_avg[1])
                        metrics_collector.record_gauge("system_load_15m", load_avg[2])

                    time.sleep(60)  # Monitor every minute

                except Exception as e:
                    self.system_logger.error(f"System monitoring error: {str(e)}")
                    time.sleep(60)

        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()

    def extract_user_context(self, request: Request) -> Dict[str, str]:
        """Extract user context from request"""
        user_context = {}

        # Try to extract user from JWT token
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                # This would require JWT decoding - simplified for now
                user_context["has_auth"] = "true"
            except Exception:
                user_context["has_auth"] = "false"
        else:
            user_context["has_auth"] = "false"

        # Extract other context
        user_context.update({
            "ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "")[:100],  # Truncate
            "endpoint": request.url.path,
            "method": request.method
        })

        return user_context

    def categorize_endpoint(self, path: str) -> str:
        """Categorize endpoint for metrics"""
        if path.startswith("/api/auth"):
            return "authentication"
        elif path.startswith("/api/cape"):
            return "ai_service"
        elif path.startswith("/api/audit"):
            return "audit"
        elif path.startswith("/api/health"):
            return "health"
        elif path.startswith("/docs") or path.startswith("/openapi"):
            return "documentation"
        elif path.startswith("/static") or path.startswith("/assets"):
            return "static"
        else:
            return "other"

    def log_request_metrics(self, request: Request, response: Response,
                           processing_time: float, user_context: Dict[str, str]):
        """Enhanced request metrics logging with real-time collection"""

        # Basic metrics
        endpoint_category = self.categorize_endpoint(request.url.path)

        # Record metrics
        metrics_collector.record_counter("http_requests_total", 1.0, {
            "method": request.method,
            "endpoint": request.url.path,
            "category": endpoint_category,
            "status_code": str(response.status_code)
        })

        metrics_collector.record_histogram("http_request_duration_seconds", processing_time, {
            "method": request.method,
            "endpoint": request.url.path,
            "category": endpoint_category
        })

        # Update internal statistics
        with metrics_collector._lock:
            metrics_collector.request_count += 1
            metrics_collector.total_response_time += processing_time

            # Endpoint statistics
            endpoint_key = f"{request.method} {request.url.path}"
            stats = metrics_collector.endpoint_stats[endpoint_key]
            stats['count'] += 1
            stats['total_time'] += processing_time
            stats['min_time'] = min(stats['min_time'], processing_time)
            stats['max_time'] = max(stats['max_time'], processing_time)

            # Status code statistics
            metrics_collector.status_code_stats[response.status_code] += 1

            # User agent statistics (simplified)
            user_agent = user_context.get("user_agent", "unknown")[:50]
            metrics_collector.user_agent_stats[user_agent] += 1

            # Track errors
            if response.status_code >= 400:
                metrics_collector.error_count += 1
                stats['error_count'] += 1

                metrics_collector.record_counter("http_errors_total", 1.0, {
                    "method": request.method,
                    "endpoint": request.url.path,
                    "status_code": str(response.status_code),
                    "category": endpoint_category
                })

            # Track slow requests
            if processing_time > self.alert_thresholds['slow_request_threshold']:
                metrics_collector.slow_request_count += 1

                metrics_collector.record_counter("http_slow_requests_total", 1.0, {
                    "method": request.method,
                    "endpoint": request.url.path,
                    "category": endpoint_category
                })

            # Store recent request info
            request_info = {
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "processing_time": round(processing_time * 1000, 2),
                "ip": user_context.get("ip", "unknown"),
                "category": endpoint_category
            }
            metrics_collector.recent_requests.append(request_info)

        # Detailed logging if enabled
        if self.enable_detailed_logging:
            detailed_metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "category": endpoint_category,
                "status_code": response.status_code,
                "processing_time_ms": round(processing_time * 1000, 2),
                "response_size": response.headers.get("content-length", 0),
                **user_context
            }

            # Log performance metrics
            self.performance_logger.info(f"API_REQUEST: {json.dumps(detailed_metrics)}")

            # Alert on slow requests
            if processing_time > self.alert_thresholds['slow_request_threshold']:
                self.logger.warning(
                    f"SLOW_REQUEST: {detailed_metrics['path']} took {processing_time:.2f}s"
                )

            # Alert on errors and track in error system
            if response.status_code >= 400:
                error_metrics = {
                    **detailed_metrics,
                    "error_type": "client_error" if response.status_code < 500 else "server_error"
                }
                self.error_logger.error(f"API_ERROR: {json.dumps(error_metrics)}")

                # Track HTTP errors in error tracking system
                self._track_http_error(request, response, processing_time, user_context)

                # Log to audit system for security events
                if response.status_code == 401 or response.status_code == 403:
                    try:
                        db = next(get_db())
                        self.audit_logger.log_security_event(
                            db=db,
                            event_type=AuditEventType.UNAUTHORIZED_ACCESS,
                            user_email=None,  # Would extract from token if available
                            ip_address=user_context.get("ip"),
                            user_agent=user_context.get("user_agent"),
                            endpoint=request.url.path,
                            http_method=request.method,
                            status_code=response.status_code,
                            success=False,
                            error_message=f"HTTP {response.status_code} error",
                            metadata={
                                "processing_time_ms": round(processing_time * 1000, 2),
                                "endpoint_category": endpoint_category
                            }
                        )
                    except Exception as e:
                        self.logger.error(f"Failed to log audit event: {str(e)}")

    def _track_http_error(self,
                         request: Request,
                         response: Response,
                         processing_time: float,
                         user_context: Dict[str, str]):
        """Track HTTP errors in the error tracking system"""

        # Only track server errors and important client errors
        if response.status_code >= 500 or response.status_code in [401, 403, 404, 429]:

            # Determine severity based on status code
            if response.status_code >= 500:
                severity = ErrorSeverity.HIGH
            elif response.status_code in [401, 403]:
                severity = ErrorSeverity.MEDIUM
            else:
                severity = ErrorSeverity.LOW

            # Determine category
            if response.status_code == 401:
                category = ErrorCategory.AUTHENTICATION
            elif response.status_code == 403:
                category = ErrorCategory.AUTHORIZATION
            elif response.status_code == 404:
                category = ErrorCategory.VALIDATION
            elif response.status_code == 429:
                category = ErrorCategory.PERFORMANCE
            else:
                category = ErrorCategory.SYSTEM

            # Track the HTTP error
            self.error_tracker.track_error(
                error_message=f"HTTP {response.status_code} error on {request.url.path}",
                severity=severity,
                category=category,
                endpoint=request.url.path,
                http_method=request.method,
                user_id=user_context.get('user_id'),
                user_agent=user_context.get('user_agent'),
                ip_address=user_context.get('ip'),
                response_status=response.status_code,
                processing_time_ms=round(processing_time * 1000, 2),
                additional_context={
                    "error_type": "http_error",
                    "endpoint_category": self.categorize_endpoint(request.url.path),
                    "response_headers": dict(response.headers)
                }
            )

    def log_business_metrics(self, request: Request, response: Response,
                            processing_time: float, user_context: Dict[str, str]):
        """Log business-specific metrics"""
        endpoint_category = self.categorize_endpoint(request.url.path)

        # Track AI service usage
        if endpoint_category == "ai_service" and response.status_code == 200:
            metrics_collector.record_counter("ai_requests_successful", 1.0, {
                "endpoint": request.url.path
            })

            # Log AI service performance
            self.business_logger.info(f"AI_SERVICE_REQUEST: {json.dumps({
                'timestamp': datetime.utcnow().isoformat(),
                'endpoint': request.url.path,
                'processing_time_ms': round(processing_time * 1000, 2),
                'ip': user_context.get('ip', 'unknown'),
                'method': request.method,
                'status_code': response.status_code
            })}")   

        # Track authentication events
        if endpoint_category == "authentication":
            if response.status_code == 200:
                metrics_collector.record_counter("auth_requests_successful", 1.0, {
                    "endpoint": request.url.path
                })
            else:
                metrics_collector.record_counter("auth_requests_failed", 1.0, {
                    "endpoint": request.url.path,
                    "status_code": str(response.status_code)
                })

    def log_security_event(self, request: Request, event_type: str, details: Dict[str, Any]):
        """Enhanced security event logging"""
        security_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "client_ip": request.client.host if request.client else "unknown",
            "path": request.url.path,
            "user_agent": request.headers.get("user-agent", ""),
            "details": details
        }

        self.security_logger.warning(f"SECURITY_EVENT: {json.dumps(security_event)}")

        # Record security metrics
        metrics_collector.record_counter("security_events_total", 1.0, {
            "event_type": event_type,
            "endpoint": request.url.path
        })

    async def dispatch(self, request: Request, call_next):
        """Enhanced request dispatching with comprehensive monitoring and error tracking"""
        start_time = time.time()

        # Extract user context
        user_context = self.extract_user_context(request)

        # Log incoming request
        if self.enable_detailed_logging:
            self.logger.info(f"Incoming {request.method} {request.url.path} from {user_context.get('ip', 'unknown')}")

        try:
            # Process request
            response = await call_next(request)
            processing_time = time.time() - start_time

            # Log comprehensive metrics
            self.log_request_metrics(request, response, processing_time, user_context)
            self.log_business_metrics(request, response, processing_time, user_context)

            return response

        except Exception as e:
            processing_time = time.time() - start_time

            # Enhanced error tracking with comprehensive context
            error_id = self._track_comprehensive_error(
                e, request, processing_time, user_context
            )

            # Log exception with error ID
            error_details = {
                "timestamp": datetime.utcnow().isoformat(),
                "error_id": error_id,
                "method": request.method,
                "path": request.url.path,
                "processing_time_ms": round(processing_time * 1000, 2),
                "error": str(e),
                "error_type": type(e).__name__,
                **user_context
            }

            self.error_logger.error(f"REQUEST_EXCEPTION: {json.dumps(error_details)}")

            # Record exception metrics
            metrics_collector.record_counter("http_exceptions_total", 1.0, {
                "method": request.method,
                "endpoint": request.url.path,
                "exception_type": type(e).__name__
            })

            # Update error statistics
            with metrics_collector._lock:
                metrics_collector.error_count += 1

            raise

    def _track_comprehensive_error(self,
                                  exception: Exception,
                                  request: Request,
                                  processing_time: float,
                                  user_context: Dict[str, str]) -> str:
        """Track error with comprehensive context using error tracking service"""

        # Determine error severity based on exception type and context
        severity = self._determine_error_severity(exception, request)

        # Determine error category
        category = self._determine_error_category(exception, request)

        # Prepare request data (safely)
        request_data = None
        try:
            if hasattr(request, 'json') and request.method in ['POST', 'PUT', 'PATCH']:
                # Don't include sensitive data in error logs
                request_data = {"method": request.method, "content_type": request.headers.get("content-type")}
        except:
            pass

        # Extract user ID from context if available
        user_id = user_context.get('user_id')

        # Track error with comprehensive context
        error_id = self.error_tracker.track_error(
            exception=exception,
            severity=severity,
            category=category,
            endpoint=request.url.path,
            http_method=request.method,
            user_id=user_id,
            session_id=user_context.get('session_id'),
            user_agent=user_context.get('user_agent'),
            ip_address=user_context.get('ip'),
            request_data=request_data,
            processing_time_ms=round(processing_time * 1000, 2),
            additional_context={
                "url_params": dict(request.query_params),
                "headers_count": len(request.headers),
                "endpoint_category": self.categorize_endpoint(request.url.path)
            }
        )

        return error_id

    def _determine_error_severity(self, exception: Exception, request: Request) -> ErrorSeverity:
        """Determine error severity based on exception type and context"""

        # Critical errors
        if isinstance(exception, (MemoryError, SystemError)):
            return ErrorSeverity.CRITICAL

        # High severity errors
        if any(keyword in str(exception).lower() for keyword in ['database', 'connection', 'timeout']):
            return ErrorSeverity.HIGH

        # Authentication/Authorization errors
        if any(keyword in str(exception).lower() for keyword in ['unauthorized', 'forbidden', 'auth']):
            return ErrorSeverity.HIGH

        # AI service errors
        if 'openai' in str(exception).lower() or '/ai/' in request.url.path:
            return ErrorSeverity.HIGH

        # Validation errors
        if isinstance(exception, ValueError) or 'validation' in str(exception).lower():
            return ErrorSeverity.MEDIUM

        # Default severity
        return ErrorSeverity.MEDIUM

    def _determine_error_category(self, exception: Exception, request: Request) -> ErrorCategory:
        """Determine error category based on exception type and context"""

        # Authentication/Authorization
        if any(keyword in str(exception).lower() for keyword in ['unauthorized', 'forbidden', 'auth', 'login']):
            if 'unauthorized' in str(exception).lower():
                return ErrorCategory.AUTHORIZATION
            else:
                return ErrorCategory.AUTHENTICATION

        # Database errors
        if any(keyword in str(exception).lower() for keyword in ['database', 'sql', 'connection']):
            return ErrorCategory.DATABASE

        # AI service errors
        if 'openai' in str(exception).lower() or '/ai/' in request.url.path:
            return ErrorCategory.AI_SERVICE

        # Network errors
        if any(keyword in str(exception).lower() for keyword in ['network', 'connection', 'timeout']):
            return ErrorCategory.NETWORK

        # Validation errors
        if isinstance(exception, ValueError) or 'validation' in str(exception).lower():
            return ErrorCategory.VALIDATION

        # Performance errors
        if 'timeout' in str(exception).lower() or 'slow' in str(exception).lower():
            return ErrorCategory.PERFORMANCE

        # Security errors
        if any(keyword in str(exception).lower() for keyword in ['security', 'xss', 'injection', 'csrf']):
            return ErrorCategory.SECURITY

        # System errors
        if isinstance(exception, (SystemError, MemoryError, OSError)):
            return ErrorCategory.SYSTEM

        # Default category
        return ErrorCategory.UNKNOWN


# Enhanced Health Check Functions
async def health_check_detailed():
    """Comprehensive health check with system metrics and application status"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Get current metrics statistics
        stats = metrics_collector.get_statistics()

        # Database health check
        db_healthy = True
        db_error = None
        try:
            db = next(get_db())
            db.execute("SELECT 1")
            db.close()
        except Exception as e:
            db_healthy = False
            db_error = str(e)

        # Application status
        app_status = {
            "version": "3.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "uptime": time.time() - (metrics_collector.metrics.get("system_start_time", [MetricPoint(datetime.utcnow(), time.time(), {}, "gauge")])[-1].value if metrics_collector.metrics.get("system_start_time") else time.time()),
            "database_connected": db_healthy,
            "database_error": db_error
        }

        # System health
        system_health = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "memory_total": memory.total,
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_total": disk.total,
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
        }

        # Overall health status
        health_status = "healthy"
        health_issues = []

        if cpu_percent > 80:
            health_status = "degraded"
            health_issues.append(f"High CPU usage: {cpu_percent}%")

        if memory.percent > 80:
            health_status = "degraded"
            health_issues.append(f"High memory usage: {memory.percent}%")

        if not db_healthy:
            health_status = "unhealthy"
            health_issues.append(f"Database connection failed: {db_error}")

        if stats['error_rate'] > 10:
            health_status = "degraded"
            health_issues.append(f"High error rate: {stats['error_rate']}%")

        return {
            "status": health_status,
            "timestamp": datetime.utcnow().isoformat(),
            "issues": health_issues,
            "system": system_health,
            "application": app_status,
            "metrics_summary": {
                "total_requests": stats['request_count'],
                "error_rate": stats['error_rate'],
                "avg_response_time": stats['avg_response_time'],
                "slow_requests": stats['slow_request_count']
            }
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "issues": [f"Health check failed: {str(e)}"]
        }


async def get_metrics_summary() -> Dict[str, Any]:
    """Get comprehensive metrics summary"""
    stats = metrics_collector.get_statistics()

    # Get recent system metrics
    cpu_metrics = metrics_collector.get_metrics("system_cpu_percent")
    memory_metrics = metrics_collector.get_metrics("system_memory_percent")

    # Calculate recent averages
    recent_cpu = 0
    recent_memory = 0

    if cpu_metrics.get("system_cpu_percent"):
        recent_values = cpu_metrics["system_cpu_percent"][-10:]  # Last 10 values
        recent_cpu = sum(point['value'] for point in recent_values) / len(recent_values)

    if memory_metrics.get("system_memory_percent"):
        recent_values = memory_metrics["system_memory_percent"][-10:]
        recent_memory = sum(point['value'] for point in recent_values) / len(recent_values)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "performance": {
            "total_requests": stats['request_count'],
            "total_errors": stats['error_count'],
            "error_rate": stats['error_rate'],
            "avg_response_time_ms": stats['avg_response_time'],
            "slow_requests": stats['slow_request_count'],
            "slow_request_rate": stats['slow_request_rate']
        },
        "system": {
            "avg_cpu_percent": round(recent_cpu, 2),
            "avg_memory_percent": round(recent_memory, 2)
        },
        "endpoints": stats['endpoint_stats'],
        "status_codes": stats['status_code_stats'],
        "recent_requests": list(metrics_collector.recent_requests)[-10:]  # Last 10 requests
    }


async def get_real_time_metrics(metric_name: Optional[str] = None,
                               minutes: int = 60) -> Dict[str, Any]:
    """Get real-time metrics for specific time window"""
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)

    all_metrics = metrics_collector.get_metrics(metric_name)

    # Filter by time window
    filtered_metrics = {}
    for name, points in all_metrics.items():
        filtered_points = [
            point for point in points
            if datetime.fromisoformat(point['timestamp'].replace('Z', '+00:00').replace('+00:00', '')) >= cutoff_time
        ]
        if filtered_points:
            filtered_metrics[name] = filtered_points

    return {
        "time_window_minutes": minutes,
        "metrics": filtered_metrics,
        "summary": {
            "total_metrics": len(filtered_metrics),
            "data_points": sum(len(points) for points in filtered_metrics.values())
        }
    }


def get_monitoring_middleware_instance() -> MonitoringMiddleware:
    """Get the monitoring middleware instance for configuration"""
    # This would be set by the main application
    return getattr(get_monitoring_middleware_instance, '_instance', None)


def set_monitoring_middleware_instance(instance: MonitoringMiddleware):
    """Set the monitoring middleware instance"""
    get_monitoring_middleware_instance._instance = instance


# Initialize system start time
if not metrics_collector.metrics.get("system_start_time"):
    metrics_collector.record_gauge("system_start_time", time.time())
