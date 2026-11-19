from flask import current_app
from pymongo import MongoClient


def init_database(app):
    mongo_uri = app.config["MONGO_URI"]
    app.extensions["mongo_client"] = (
        MongoClient(mongo_uri, serverSelectionTimeoutMS=2000) if mongo_uri else None
    )


def get_sentiment_collection():
    client = current_app.extensions["mongo_client"]
    if client is None:
        return None
    return client[current_app.config["MONGO_DB_NAME"]]["sentiment_history"]
