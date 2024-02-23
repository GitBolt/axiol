import random
from constants import DEFAULT_PREFIX
from database import PREFIXES, LEVEL_DATABASE, PLUGINS, PERMISSIONS


async def get_prefix(ctx):
    prefix = await PREFIXES.find_one({"_id": ctx.guild.id})

    if prefix is not None:
        return prefix["prefix"]
    else:
        return DEFAULT_PREFIX


async def get_xp_range(guild_id):
    collection = LEVEL_DATABASE.get_collection(str(guild_id))
    settings = await collection.find_one({"_id": 0})
    return settings["xprange"]


async def get_random_text(typing_time):
    f = open("resources/words.txt").read()
    words = f.split("\n")

    if typing_time == 10:
        r = range(15)

    elif typing_time == 15:
        r = range(25)

    elif typing_time == 30:
        r = range(40)

    elif typing_time == 60:
        r = range(60)

    else:
        r = range(1)

    return " ".join(random.choice(words) for i in r)


def get_code(amount):
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=amount))


"""
Below are some functions to counter errors and warnings while working locally.

To get everything to work properly, local database needs to be sync, even if it's 
working locally on a single guild.

update_plugins_and_permissions() function simply updates all plugin and permissions documents with a new
plugin, only used when some new plugin is added. Not required to use this 
function to fix any errors or warnings.

update_db() does the main job, it checks for all plugin, permission, 
leveling (if enabled) and prefix documents, then updates/adds them if they
aren't there.

I would have loved to say that I did this intentionally to avoid people from 
stealing code but it was just me writing bad code which ended up benefiting
¯\_(ツ)_/¯
"""


# Adding new plugin and permissions
async def update_plugins_and_permissions(plugin):
    await PLUGINS.update_many({plugin: {"$exists": False}}, {"$set": {plugin: True}})
    await PERMISSIONS.update_many({plugin: {"$exists": False}}, {"$set": {plugin: {}}})


# updating leveling, plugin, prefix and permission data
async def update_db(guild_ids):
    plugins_update = []
    permissions_update = []
    leveling_update = []

    for guild_id in guild_ids:

        if not await PLUGINS.count_documents({"_id": guild_id}, limit=1):
            PLUGINS.insert_one(
                {
                    "_id": guild_id,
                    "Leveling": False,
                    "Moderation": True,
                    "ReactionRoles": True,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": True,
                    "AutoMod": False,
                    # "Karma": False,
                    "Fun": True,
                    "Giveaway": True,
                }
            )
            plugins_update.append(guild_id)
            print(f"✅{guild_id} - Plugins 🔧")

        if not await PERMISSIONS.count_documents({"_id": guild_id}, limit=1):
            PERMISSIONS.insert_one(
                {
                    "_id": guild_id,
                    "Leveling": {},
                    "Moderation": {},
                    "ReactionRoles": {},
                    "Welcome": {},
                    "Verification": {},
                    "Chatbot": {},
                    "Commands": {},
                    "AutoMod": {},
                    # "Karma": {},
                    "Fun": {},
                    "Giveaway": {},
                }
            )
            permissions_update.append(guild_id)
            print(f"✅{guild_id} - Permissions 🔨")

        guild_plugins = await PLUGINS.find_one({"_id": guild_id})
        if (
            guild_plugins["Leveling"]
            and str(guild_id) not in await LEVEL_DATABASE.list_collection_names()
        ):
            guild_level_db = await LEVEL_DATABASE.create_collection(str(guild_id))
            await guild_level_db.insert_one(
                {
                    "_id": 0,
                    "xprange": [15, 25],
                    "alertchannel": None,
                    "blacklistedchannels": [],
                    "alerts": True,
                }
            )
            leveling_update.append(guild_id)
            print(f"✅{guild_id} - Leveling 📊")

        # Only use this when working locally
        try:
            await PREFIXES.insert_one({"_id": guild_id, "prefix": "ax"})
            print(f"✅{guild_id} - Prefix ⚪")

        except:
            print(f"❌{guild_id} - Prefix ⚪")

    print(
        f"Update results"
        f"\n{len(plugins_update)} plugins\n"
        f"{len(permissions_update)} permissions\n"
        f"{len(leveling_update)} leveling"
    )
