import os

#Config
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "."
YTAPI_KEY = os.environ.get("YTAPI_KEY")

#Colours
C_MAIN = 0xFF006A #Everything Bot Related
C_GREEN = 0x15ff00 #Success
C_RED = 0xFF0000 #Error
C_ORANGE = 0xFF4400 #Warning
C_BLUE = 0x00AEFF #Showing data
C_TEAL = 0x00EEFF #Everything else

#Emojis
E_LOGO = "<:Logo:845663121477206036>"
E_ACCEPT = "<:Accept:847850079968559175>"
E_DECLINE = "<:Decline:847850006995402822>"
E_ENABLE = "<:Enable:847850083819323442>"
E_DISABLE = "<:Disable:847850081700020254>"
E_SETTINGS = "<:Settings:847850081965178901>"
E_CONTINUE = "<:Continue:847850081587167234>"
#Extra Emoji
E_LOADING = "<a:loading:854065859667165235>"
E_ERROR = "<:Error:849342766898610196>"
E_LEVELING = "<:Icon:846436455496941588>"
E_BOT = "<:BotVerification:846990577442095114>"
E_PLUGINS = "<:Plugins:849660552116174888>"
#Colour Emojis
E_RED = "<:red:846068024050319440>"
E_PINK = "<:pink:846386699730419742>"
E_GREEN = "<:green:846068024511037468>"
E_BLUE = "<:blue:846068023660249088>"
E_ORANGE = "<:orange:846068023814914059>"
E_YELLOW = "<:yellow:846068023675846688>"
E_RECYCLE = "<:recycle:853300271944695858>"


DICT_PLUGINEMOJIS = {
    "Leveling": E_LEVELING,
    "Moderation": "🔨",
    "Reaction Roles": "✨",
    "Welcome": "👋",
    "Verification": "✅",
    "Chatbot": "🤖",
    "Music": "🎵",
}

