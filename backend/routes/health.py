from flask import Blueprint, current_app, jsonify
from pymongo.errors import PyMongoError


health_bp = Blueprint("health", __name__)


@health_bp.get("/api/health")
def health():
    client = current_app.extensions["mongo_client"]
    if client is None:
        return jsonify(
            {
                "status": "ok",
                "database": "not_configured",
                "message": "API is running; results will not be persisted.",
            }
        )

    try:
        client.admin.command("ping")
    except PyMongoError:
        current_app.logger.exception("MongoDB health check failed")
        return jsonify(
            {
                "status": "degraded",
                "database": "unavailable",
                "message": "MongoDB is configured but could not be reached.",
            }
        ), 503

    return jsonify({"status": "ok", "database": "connected"})
