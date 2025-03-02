import bson
from flask import Flask, g
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from application import application as app
from server.settings.config import Config


app.config["MONGO_URI"] = Config.MONGO_URI


mongo = PyMongo(app)


def get_mongo_db_instance():
    """
    Returns the MongoDB instance, ensuring only one connection per request.
    """
    if not hasattr(g, "_database"):
        g._database = mongo.db
    return g._database


mongo_db = LocalProxy(get_mongo_db_instance)  # Global db proxy


@app.teardown_appcontext
def close_connection(exception=None):
    """
    Ensures the database connection is properly closed after each request.
    """
    db_client = getattr(g, "_database", None)
    if db_client is not None:
        db_client.client.close()
