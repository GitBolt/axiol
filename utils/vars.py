import os
from pymongo import MongoClient

#Config
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "."

#DB
MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL")) #Client
DATABASE = MONGOCLIENT["Axiol"] #Main Cluster
LEVELDATABASE = MONGOCLIENT["Leveling"] #Leveling Cluster
#Collections
PREFIXES = DATABASE["Prefixes"]
REACTIONROLES = DATABASE["Reaction Roles"]
VERIFY = DATABASE["Verify"]

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

#Emojis
SETTINGS = "<:settings:843518099842924584>"
LOGO = "<:logo:843531246936129546>"
DELETE = "<:delete:843531621915426846>"