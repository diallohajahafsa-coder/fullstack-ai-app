import os
import re
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import PyMongoError


POSITIVE_WORDS = {
    "amazing",
    "awesome",
    "best",
    "excellent",
    "good",
    "great",
    "happy",
    "love",
    "wonderful",
}
NEGATIVE_WORDS = {
    "awful",
    "bad",
    "disappointing",
    "hate",
    "poor",
    "sad",
    "terrible",
    "worst",
}


def analyze_sentiment(text):
    words = [re.sub(r"[^a-z]", "", word) for word in text.lower().split()]
    positive_count = sum(word in POSITIVE_WORDS for word in words)
    negative_count = sum(word in NEGATIVE_WORDS for word in words)
    difference = positive_count - negative_count

    if difference > 0:
        label = "positive"
    elif difference < 0:
        label = "negative"
    else:
        label = "neutral"

    matched_count = positive_count + negative_count
    strength = round(abs(difference) / matched_count, 2) if matched_count else 0
    return {"label": label, "strength": strength, "mode": "demo_rules"}


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        MONGO_URI=os.getenv("MONGO_URI", "").strip(),
        MONGO_DB_NAME=os.getenv("MONGO_DB_NAME", "ai_fullstack"),
        FRONTEND_ORIGIN=os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
    )
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}})

    mongo_client = None
    if app.config["MONGO_URI"]:
        mongo_client = MongoClient(
            app.config["MONGO_URI"],
            serverSelectionTimeoutMS=2000,
        )
    app.extensions["mongo_client"] = mongo_client

    @app.get("/api/health")
    def health():
        if mongo_client is None:
            return jsonify(
                {
                    "status": "ok",
                    "database": "not_configured",
                    "message": "API is running; results will not be persisted.",
                }
            )

        try:
            mongo_client.admin.command("ping")
        except PyMongoError:
            app.logger.exception("MongoDB health check failed")
            return jsonify(
                {
                    "status": "degraded",
                    "database": "unavailable",
                    "message": "MongoDB is configured but could not be reached.",
                }
            ), 503

        return jsonify({"status": "ok", "database": "connected"})

    @app.post("/api/sentiment")
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

        if mongo_client is None:
            result["storage"] = "not_configured"
            return jsonify(result)

        try:
            collection = mongo_client[app.config["MONGO_DB_NAME"]]["sentiment_history"]
            collection.insert_one(
                {
                    **result,
                    "created_at": datetime.now(timezone.utc),
                }
            )
        except PyMongoError:
            app.logger.exception("Could not save sentiment analysis")
            return jsonify(
                {"error": "MongoDB is unavailable; the analysis was not saved."}
            ), 503

        result["stored"] = True
        result["storage"] = "mongodb"
        return jsonify(result)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        port=int(os.getenv("PORT", "5000")),
    )
