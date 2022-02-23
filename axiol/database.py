import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_CLIENT = AsyncIOMotorClient(os.environ["MONGO_URL"])

# Databases
DATABASE = MONGO_CLIENT["Axiol"]  # Main DB
LEVEL_DATABASE = MONGO_CLIENT["Leveling"]
KARMA_DATABASE = MONGO_CLIENT["Karma"]
CUSTOM_DATABASE = MONGO_CLIENT["Custom"]
WARNINGS_DATABASE = MONGO_CLIENT["Warnings"]

# Collections
PLUGINS = DATABASE["Plugins"]
PREFIXES = DATABASE["Prefixes"]
REACTION_ROLES = DATABASE["Reaction Roles"]
WELCOME = DATABASE["Welcome"]
VERIFY = DATABASE["Verify"]
CHATBOT = DATABASE["Chatbot"]
PERMISSIONS = DATABASE["Permissions"]
AUTO_MOD = DATABASE["AutoMod"]
GIVEAWAY = DATABASE["Giveaway"]
LOGGING = DATABASE["Logging"]
