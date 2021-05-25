from .vars import PREFIXES, DEFAULT_PREFIX, LEVELDATABASE

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

