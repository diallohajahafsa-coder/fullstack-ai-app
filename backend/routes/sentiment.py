from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request
from pymongo.errors import PyMongoError

from db import get_sentiment_collection
from services.sentiment_service import analyze_sentiment


sentiment_bp = Blueprint("sentiment", __name__)


@sentiment_bp.post("/api/sentiment")
def sentiment():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return jsonify({"error": "A JSON string field named 'text' is required."}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Text must not be empty."}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text must be 5,000 characters or fewer."}), 400

    result = {
        "text": text,
        **analyze_sentiment(text),
        "stored": False,
    }

    collection = get_sentiment_collection()
    if collection is None:
        result["storage"] = "not_configured"
        return jsonify(result)

    try:
        collection.insert_one(
            {
                **result,
                "created_at": datetime.now(timezone.utc),
            }
        )
    except PyMongoError:
        current_app.logger.exception("Could not save sentiment analysis")
        return jsonify(
            {"error": "MongoDB is unavailable; the analysis was not saved."}
        ), 503

    result["stored"] = True
    result["storage"] = "mongodb"
    return jsonify(result)
