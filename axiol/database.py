import os
from motor.motor_asyncio import AsyncIOMotorClient


MONGOCLIENT = AsyncIOMotorClient(os.environ["MONGO_URL"])

#Databases
DATABASE = MONGOCLIENT["Axiol"] #Main DB
LEVELDATABASE = MONGOCLIENT["Leveling"]
KARMADATBASE = MONGOCLIENT["Karma"]
CUSTOMDATABASE = MONGOCLIENT["Custom"]
WARNINGSDATABASE = MONGOCLIENT["Warnings"]

#Collections
PLUGINS = DATABASE["Plugins"]
PREFIXES = DATABASE["Prefixes"]
REACTIONROLES = DATABASE["Reaction Roles"]
WELCOME = DATABASE["Welcome"]
VERIFY = DATABASE["Verify"]
CHATBOT = DATABASE["Chatbot"]
PERMISSIONS = DATABASE["Permissions"]
AUTOMOD = DATABASE["AutoMod"]
GIVEAWAY = DATABASE["Giveaway"]