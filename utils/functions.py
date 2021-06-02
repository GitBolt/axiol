from utils.variables import DEFAULT_PREFIX
from utils.database import PREFIXES, LEVELDATABASE, PLUGINS

def getprefix(ctx):
    try:
        return PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
    except AttributeError:
        return DEFAULT_PREFIX
    
def getxprange(message):
    col = LEVELDATABASE.get_collection(str(message.guild.id))
    settings = col.find_one({"_id": 0})
    xprange =settings.get("xprange")
    return xprange



#Some functions to counter errors and warning while working locally :p
def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )

def updatedb(serverid):
    try:
        GuildLevelDB = LEVELDATABASE.create_collection(str(serverid))
        GuildLevelDB.insert_one({

            "_id": 0,
            "xprange": [15, 25],
            "alertchannel": None,
            "blacklistedchannels": [],
            }) 
        print(f"Added Leveling {serverid}")

        PLUGINS.insert_one({

                    "_id":serverid,
                    "Leveling":True,
                    "Moderation": True,
                    "Reaction Roles": True,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": False,
                })
        print(f"Added Plugins {serverid}")

    except:
        print(f"Already there {serverid}")

"""
serveridlist = []
for i in serveridlist:
    updatedb(843516084266729512)
updateplugins()

"""