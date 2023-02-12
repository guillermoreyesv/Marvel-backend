from application import app
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

# DATABASE CONFIG
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
