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


async def leaderboardpagination(ctx, current_page, embed, GuildCol, all_pages):
    pagern = current_page + 1
    embed.set_footer(text=f"Page {pagern}/{all_pages}")
    embed.clear_fields()

    rankings = GuildCol.find({

            "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
            
        }).sort("xp", -1)

    rankcount = (current_page)*10
    user_amount = current_page*10
    for i in rankings[user_amount:]:
        rankcount += 1
        getuser = ctx.guild.get_member(i.get("_id"))
        xp = i.get("xp")
        if getuser == None:
            user = "🚫 This user has left the server"
        else:
            user = getuser
        embed.add_field(name=f"{rankcount}: {user}", value=f"Total XP: {xp}", inline=False)
        if rankcount == (current_page)*10 + 10:
            break


async def reactionrolespagination(current_page, all_pages, embed, Guild, GuildDoc):
    pagern = current_page + 1
    embed.set_footer(text=f"Page {pagern}/{all_pages}")
    embed.clear_fields()

    rrcount = (current_page)*10
    rr_amount = current_page*10

    for i in GuildDoc["reaction_roles"][rr_amount:]:
        rrcount += 1
        messageid = i.get("messageid")
        role = Guild.get_role(i.get("roleid"))
        emoji = i.get("emoji")
        embed.add_field(name=f"** **", value=f"{emoji} for {role.mention}\nMessageID: `{messageid}`", inline=False)

        if rrcount == (current_page)*10 + 10:
            break




#Some functions to counter errors and warning while working locally :p

#Adding new plugin
def updateplugins(plugin):
    PLUGINS.update_many(
        { plugin: { "$exists": False } },
            {
                "$set": { plugin : False }
            }
    )


#updating leveling, plugin and permission data
def updatedb(serverid):

    if not PLUGINS.count_documents({"_id": serverid}, limit=1):
        PLUGINS.insert_one({

                    "_id":serverid,
                    "Leveling":False,
                    "Moderation": False,
                    "Reaction Roles": False,
                    "Welcome": False,
                    "Verification": False,
                    "Chatbot": False,
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
        })
        print(f"✅{serverid} - Permissions 🔨")


    if PLUGINS.find_one({"_id": serverid}).get("Leveling"):
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
            print(f"❌{serverid} - Leveling 📊")
    
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
#updateplugins("")