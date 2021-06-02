import os
from utils.database import LEVELDATABASE

#Config
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "."

#Colours
CMAIN = 0xFF006A #Everything
CGREEN = 0x15ff00 #Success
CRED = 0xFF0000 #Error
CORANGE = 0xFF4400 #Warning
CBLUE = 0x00AEFF #Data
CTEAL = 0x00EEFF #Data

#Emojis
LOGO = "<:Logo:845663121477206036>"
ACCEPT = "<:Accept:847850079968559175>"
DECLINE = "<:Decline:847850006995402822>"
ENABLE = "<:Enable:847850083819323442>"
DISABLE = "<:Disable:847850081700020254>"
SETTINGS = "<:Settings:847850081965178901>"
CONTINUE = "<:Continue:847850081587167234>"
#Extra Emoji
ERROR = "<:Error:849342766898610196>"
LVL = "<:Icon:846436455496941588>"
BOT = "<:BotVerification:846990577442095114>"
PLUGINSEMOJI = "<:Plugins:849660552116174888>"
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
    "Welcome": "👋",
    "Verification": ACCEPT,
    "Chatbot": "🤖",
}

