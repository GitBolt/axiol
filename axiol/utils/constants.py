from enum import Enum

class Colours(Enum):
    GREEN = 0x15ff00  # Success
    ORANGE = 0xFF4400  # Warning
    RED = 0xFF0000  # Error
    MAIN = 0xFF006A  # Everything bot related
    BLUE = 0x00AEFF  # Showing data/information

class Emojis(Enum):
    LOGO = "<:Logo:845663121477206036>"
    ACCEPT = "<:Accept:847850079968559175>"
    DECLINE = "<:Decline:847850006995402822>"
    ENABLE = "<:Enable:847850083819323442>"
    DISABLE = "<:Disable:847850081700020254>"
    SETTINGS = "<:Settings:860554043284914218>"
    PLUGINS = "<:Plugins:860556457615294474>"
    EVELING = "<:leveling:879026839794892881>"
    CONTINUE = "<:Continue:847850081587167234>"
    LOADING = "<a:Loading:854065859667165235>"
    RECYCLE = "<:recycle:853300271944695858>"
    BOT = "<:BotVerification:846990577442095114>"

class ColorEmojis(Enum):
    RED = "<:red:846068024050319440>"
    PINK = "<:pink:846386699730419742>"
    GREEN = "<:green:846068024511037468>"
    BLUE = "<:blue:846068023660249088>"
    ORANGE = "<:orange:846068023814914059>"
    YELLOW = "<:yellow:846068023675846688>"

class PluginsEmoji(Enum):
    "Leveling"= "<:leveling:879026839794892881>",
    "Moderation"= "🔨",
    "ReactionRoles"= "✨",
    "Welcome"= "👋",
    "Verification"= "✅",
    "Chatbot"= "🤖",
    "AutoMod"= "🛡️",
    "Karma"= "🎭",
    "Fun"= "🎯",
    "Giveaway"= "🎉",
