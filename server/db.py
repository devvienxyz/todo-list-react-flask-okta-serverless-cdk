from flask_pymongo import PyMongo
from application import application as app
from server.settings.config import Config


app.config["MONGO_URI"] = Config.MONGO_URI

mongo = PyMongo(app)
