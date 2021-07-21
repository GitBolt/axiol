import random
from variables import DEFAULT_PREFIX
from database import PREFIXES, LEVELDATABASE, PLUGINS, PERMISSIONS

def getprefix(ctx):
    try:
        return PREFIXES.find_one({"_id": ctx.guild.id}).get("prefix")
    except AttributeError:
        return DEFAULT_PREFIX
    

def getxprange(message):
    col = LEVELDATABASE.get_collection(str(message.guild.id))
    settings = col.find_one({"_id": 0})
    xprange =settings.get("xprange")
    return xprange


def random_text(typing_time):
    f = open("resources/all_text.txt").read()
    words = f.split(" ")

    if typing_time > 30:
        r = range(typing_time+30)
    else:
        r = range(typing_time)

    text = " ".join([random.choice(words) for i in r])
    return text


"""
Some functions to counter errors and warnings while working locally :p

To get everything work properly database needs to be updates even if it's working locally
on a single guild, this is because lots of places have major database dependencies.

First function simply updates all plugin and permissions documents with a new plugin, only used when some new plugin is added,
not required to use this function to fix any errors or warnings.

Second function does the main job, it checks for all plugin, permission, leveling (if enabled) and prefix documents,
then updates/adds them if they aren't there.

I would have loved to say that I did this intentionally to avoid people from stealing code but it was just me writing bad code
which ended up benefiting ¯\_(ツ)_/¯
"""

#Adding new plugin and permissions
def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )
    PERMISSIONS.update_many(
        { plugin: {"$exists": False} },
        {
            "$set": { plugin: {}}
        }
        
        )

#updating leveling, plugin, prefix and permission data
def updatedb(serverid):

    if not PLUGINS.count_documents({"_id": serverid}, limit=1):
        PLUGINS.insert_one({

            "_id": serverid,
            "Leveling": False,
            "Moderation": True,
            "Reaction Roles": True,
            "Welcome": False,
            "Verification": False,
            "Chatbot": True,
            "AutoMod": False,
            "Karma": False,
            "Fun": True,
        })

        print(f"✅{serverid} - Plugins 🔧")

    
    if not PERMISSIONS.count_documents({"_id": serverid}, limit=1):
        PERMISSIONS.insert_one({

            "_id": serverid,
            "Leveling": {},
            "Moderation": {},
            "Reaction Roles": {},
            "Welcome": {},
            "Verification": {},
            "Chatbot": {},
            "Commands": {},
            "AutoMod": {},
            "Karma": {},
            "Fun": {},
        })
        print(f"✅{serverid} - Permissions 🔨")


    if PLUGINS.find_one({"_id": serverid})["Leveling"]:
        try:
            GuildLevelDB = LEVELDATABASE.create_collection(str(serverid))
            GuildLevelDB.insert_one({

                "_id": 0,
                "xprange": [15, 25],
                "alertchannel": None,
                "blacklistedchannels": [],
                "alerts": True
                }) 
            print(f"✅{serverid} - Leveling 📊")
        except:
            pass
    
    try:
        PREFIXES.insert_one({
            "_id": serverid,
            "prefix": "ax"
        })
        print(f"✅{serverid} - Prefix ⚪")

    except:
        print(f"❌{serverid} - Prefix ⚪")


serveridlist = []
#for i in serveridlist:
   #updatedb(i)

#updateplugins("Karma")