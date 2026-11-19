import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from db import init_database
from routes.health import health_bp
from routes.sentiment import sentiment_bp


def create_app(test_config=None):
    load_dotenv(Path(__file__).with_name(".env"))
    app = Flask(__name__)
    app.config.from_mapping(
        MONGO_URI=os.getenv("MONGO_URI", "").strip(),
        MONGO_DB_NAME=os.getenv("MONGO_DB_NAME", "ai_fullstack"),
        FRONTEND_ORIGIN=os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
    )
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}})
    init_database(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(sentiment_bp)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        port=int(os.getenv("PORT", "5000")),
    )
