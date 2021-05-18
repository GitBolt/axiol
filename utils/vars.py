import os
from pymongo import MongoClient


DEFAULT_PREFIX = "!"
MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL"))
TOKEN = os.environ.get("TOKEN")

#Colours
TEAL = 0x00ffff
TEAL2 = 0x00d0ff
BLUE = 0x0091ff
BLUE2 = 0x005eff
MAGENTA = 0xff006f
MAGENTA2 = 0xff00d0
MAGENTA3 = 0xff4df3
RED = 0xff0000
ORANGE = 0xff6600
GREEN = 0x00ff11