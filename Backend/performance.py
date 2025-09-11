import time
import logging
import psutil
import os
from functools import wraps
from typing import Dict, Any
from flask import request, g

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.process = psutil.Process(os.getpid())
    
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        """Record a performance metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        
        metric = {
            'value': value,
            'timestamp': time.time(),
            'tags': tags or {}
        }
        
        self.metrics[name].append(metric)
        
        # Keep only last 1000 metrics per name
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        try:
            memory_info = self.process.memory_info()
            cpu_percent = self.process.cpu_percent()
            
            return {
                'memory_rss_mb': memory_info.rss / 1024 / 1024,
                'memory_vms_mb': memory_info.vms / 1024 / 1024,
                'cpu_percent': cpu_percent,
                'num_threads': self.process.num_threads(),
                'open_files': len(self.process.open_files()),
                'connections': len(self.process.connections())
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of recorded metrics."""
        summary = {}
        
        for name, values in self.metrics.items():
            if not values:
                continue
                
            recent_values = [m['value'] for m in values[-100:]]  # Last 100 values
            
            summary[name] = {
                'count': len(values),
                'avg': sum(recent_values) / len(recent_values),
                'min': min(recent_values),
                'max': max(recent_values),
                'recent_count': len(recent_values)
            }
        
        return summary

# Global monitor instance
monitor = PerformanceMonitor()

def measure_time(metric_name: str = None, tags: Dict[str, str] = None):
    """Decorator to measure function execution time."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                status = 'success'
            except Exception as e:
                status = 'error'
                raise
            finally:
                duration = time.time() - start_time
                name = metric_name or f"{func.__module__}.{func.__name__}"
                
                metric_tags = {'status': status}
                if tags:
                    metric_tags.update(tags)
                
                monitor.record_metric(f"{name}.duration", duration, metric_tags)
                
                if duration > 1.0:  # Log slow operations
                    logger.warning(f"Slow operation: {name} took {duration:.2f}s")
            
            return result
        return wrapper
    return decorator

def track_request_metrics():
    """Flask before/after request handlers for tracking metrics."""
    def before_request():
        g.start_time = time.time()
        g.start_memory = monitor.process.memory_info().rss
    
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            endpoint = request.endpoint or 'unknown'
            method = request.method
            status_code = response.status_code
            
            # Record request metrics
            tags = {
                'endpoint': endpoint,
                'method': method,
                'status_code': str(status_code)
            }
            
            monitor.record_metric('request.duration', duration, tags)
            monitor.record_metric('request.count', 1, tags)
            
            # Memory usage
            if hasattr(g, 'start_memory'):
                memory_delta = monitor.process.memory_info().rss - g.start_memory
                monitor.record_metric('request.memory_delta', memory_delta, tags)
            
            # Log slow requests
            if duration > 2.0:
                logger.warning(f"Slow request: {method} {request.path} took {duration:.2f}s")
        
        return response
    
    return before_request, after_request