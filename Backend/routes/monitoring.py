from flask import Blueprint, jsonify

from utils.cache import cache
from utils.performance import monitor

monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")


@monitoring_bp.route("/health", methods=["GET"])
def health_check():
    """Enhanced health check with system status"""
    system_metrics = monitor.get_system_metrics()

    health_status = {
        "status": "healthy",
        "service": "etoaudiobook-api",
        "system": {
            "cpu_percent": system_metrics.get("cpu_percent", 0),
            "memory_percent": system_metrics.get("memory_percent", 0),
            "disk_usage": system_metrics.get("disk_usage", {}),
        },
        "cache": {
            "enabled": cache.enabled,
            "redis_available": cache.redis_client is not None,
        },
    }

    # Determine overall health
    cpu_ok = system_metrics.get("cpu_percent", 0) < 80
    memory_ok = system_metrics.get("memory_percent", 0) < 85

    if not (cpu_ok and memory_ok):
        health_status["status"] = "degraded"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code


@monitoring_bp.route("/metrics", methods=["GET"])
def get_detailed_metrics():
    """Detailed performance metrics"""
    system_metrics = monitor.get_system_metrics()
    metrics_summary = monitor.get_metrics_summary()

    return jsonify(
        {
            "system": system_metrics,
            "application": metrics_summary,
            "cache_stats": {
                "enabled": cache.enabled,
                "redis_available": cache.redis_client is not None,
            },
            "performance_tips": _get_performance_recommendations(system_metrics),
        }
    )


def _get_performance_recommendations(system_metrics):
    """Generate performance recommendations based on current metrics"""
    recommendations = []

    cpu_percent = system_metrics.get("cpu_percent", 0)
    memory_percent = system_metrics.get("memory_percent", 0)

    if cpu_percent > 70:
        recommendations.append(
            "Consider scaling horizontally or optimizing CPU-intensive operations"
        )

    if memory_percent > 80:
        recommendations.append(
            "Memory usage is high - consider increasing available RAM or optimizing memory usage"
        )

    if not cache.redis_client:
        recommendations.append(
            "Redis cache is not available - performance may be degraded"
        )

    return recommendations
