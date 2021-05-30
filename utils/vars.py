import os
from pymongo import MongoClient

#Config
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "."

#All Database Stuff
MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL")) #Client
#Databases
DATABASE = MONGOCLIENT["Axiol"] #Main DB
LEVELDATABASE = MONGOCLIENT["Leveling"]
#Collections
PREFIXES = DATABASE["Prefixes"]
PLUGINS = DATABASE["Plugins"]
REACTIONROLES = DATABASE["Reaction Roles"]
VERIFY = DATABASE["Verify"]
WELCOME = DATABASE["Welcome"]

#Colours
CMAIN = 0xFF006A #Everything
CRED = 0xFF0000 #Error or alert
CGREEN = 0x15ff00 #Success
CORANGE = 0xFF4400 #Inform or warning
CBLUE = 0x00AEFF #Data
CTEAL = 0x00EEFF #Data

#Emojis
LOGO = "<:Logo:845663121477206036>"
ACCEPT = "<:Accept:847850079968559175>"
DECLINE = "<:Decline:847850006995402822>"
ENABLE = "<:Enable:847850083819323442>"
DISABLE = "<:Disable:847850081700020254>"
ERROR = "<:Error:847848749459439697>"
SETTINGS = "<:Settings:847850081965178901>"
CONTINUE = "<:Continue:847850081587167234>"
#Extra Emoji
LVL = "<:Icon:846436455496941588>"
BOT = "<:BotVerification:846990577442095114>"
#Colour Emojis
ERED = "<:red:846068024050319440>"
EPINK = "<:pink:846386699730419742>"
EGREEN = "<:green:846068024511037468>"
EBLUE = "<:blue:846068023660249088>"
EORANGE = "<:orange:846068023814914059>"
EYELLOW = "<:yellow:846068023675846688>"

PLUGINEMOJIS = {
    "Leveling": LVL,
    "Moderation": "🔨",
    "Reaction Roles": "✨",
    "Verification": ACCEPT,
    "Welcome": "👋",
}
