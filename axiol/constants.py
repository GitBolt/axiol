import os
import random
from typing import List


# Config
TOKEN = os.environ["TOKEN"]
DEFAULT_PREFIX = "."

# Colours
C_MAIN = 0xFF006A  # Everything Bot Related
C_GREEN = 0x15ff00  # Success
C_RED = 0xFF0000  # Error
C_ORANGE = 0xFF4400  # Warning
C_BLUE = 0x00AEFF  # Showing data
C_TEAL = 0x00EEFF  # Everything else

# Emojis
E_LOGO = "<:Logo:845663121477206036>"
E_ACCEPT = "<:Accept:847850079968559175>"
E_DECLINE = "<:Decline:847850006995402822>"
E_ENABLE = "<:Enable:847850083819323442>"
E_DISABLE = "<:Disable:847850081700020254>"
E_SETTINGS = "<:Settings:860554043284914218>"
E_PLUGINS = "<:Plugins:860556457615294474>"
E_CONTINUE = "<:Continue:847850081587167234>"

# Extra Emoji
E_LOADING = "<a:Loading:854065859667165235>"
E_LEVELING = "<:leveling:879026839794892881>"
E_BOT = "<:BotVerification:846990577442095114>"

# Colour Emojis
E_RED = "<:red:846068024050319440>"
E_PINK = "<:pink:846386699730419742>"
E_GREEN = "<:green:846068024511037468>"
E_BLUE = "<:blue:846068023660249088>"
E_ORANGE = "<:orange:846068023814914059>"
E_YELLOW = "<:yellow:846068023675846688>"
E_RECYCLE = "<:recycle:853300271944695858>"

DICT_PLUGIN_EMOJIS = {
    "Leveling": E_LEVELING,
    "Moderation": "🔨",
    "ReactionRoles": "✨",
    "Welcome": "👋",
    "Verification": "✅",
    "Chatbot": "🤖",
    "AutoMod": "🛡️",
    # "Karma": "🎭",
    "Fun": "🎯",
    "Giveaway": "🎉",
}


greeting_list: List[str] = [

    '{member} We hope you brought some milk 🥛',
    '{member} Hopped into the server!',
    '{member} Glad to have you here today!',
    'We hope you brought some sweets 🍩 {member}',
    'Have a pizza slice 🍕 {member}',
    '{member} Woooohooo! '
    'We are excited to have you here <a:hyper_cat:809781548210978828>',
    '{member} just joined, hide your cookies!🍪',
    'Swooooooosh! {member} just landed ✈',
    '{member} joined the party <a:party_parrot:810545477668962315>',
    'Roses are red, violets are blue,'
    ' {member} hopped into the server, are they a kangaroo 🦘? ',

]


def greeting(member) -> str:
    return random.choice(greeting_list).format(member=member)
