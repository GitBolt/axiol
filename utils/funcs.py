from utils.vars import DEFAULT_PREFIX
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

def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )

def updatedb(serverid):
    if serverid not in LEVELDATABASE.list_collection_names():
        GuildLevelDB = LEVELDATABASE.create_collection(str(serverid))
        GuildLevelDB.insert_one({

            "_id": 0,
            "xprange": [15, 25],
            "alertchannel": None,
            "blacklistedchannels": [],
            }) 

    if not PLUGINS.count_documents({"_id": serverid}, limit=1):
        PLUGINS.insert_one({

                    "_id":serverid,
                    "Leveling":True,
                    "Moderation": True,
                    "Reaction Roles": True,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": False,
                })


#updatedb(843516084266729512)
#updateplugins()