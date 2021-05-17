import os
from pymongo import MongoClient


DEFAULT_PREFIX = "."

MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL"))

TOKEN = os.environ.get("TOKEN")