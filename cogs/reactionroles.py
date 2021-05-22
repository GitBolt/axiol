import discord
from discord.ext import commands
import utils.vars as var


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['reactionrole', 'addrr', 'addreactionrole', 'rradd', 'reactionroleadd'])
    @commands.has_permissions(administrator=True)
    async def rr(self, ctx, msg:discord.Message=None, role: discord.Role=None, emoji=None):

        if msg and role and emoji is not None:
            guildrr = var.REACTIONROLES.find_one({"_id": ctx.guild.id})
            if guildrr == None:
                var.REACTIONROLES.insert_one({

                    "_id": ctx.guild.id,
                    "reaction_roles": [{
                        "messageid": msg.id,
                        "roleid": role.id,
                        "emoji": str(emoji)
                        }],
                    "unique_messages":[]

                    })

                await msg.add_reaction(emoji)
                await ctx.send(f"Reaction role for {role} using {emoji} setted up! https://discord.com/channels/{ctx.message.guild.id}/{msg.channel.id}/{msg.id}")
            else:
                guildrrlist = guildrr["reaction_roles"]
                for i in guildrrlist: 
                    if i.get("messageid") == msg.id and i.get("emoji") == str(emoji):
                        check = True
                    else:
                        check = False
                if check == True:
                    await ctx.send(f"You have already setted up this reaction role using {emoji} on that message :D I can see it in the database!")
                else:
                    newlist = guildrrlist.copy()
                    newlist.append({"messageid":msg.id, "roleid": role.id, "emoji": str(emoji)})
                    newdata = {"$set":{
                        "reaction_roles": newlist
                    }}
                    var.REACTIONROLES.update_one(guildrr, newdata)
                    await msg.add_reaction(emoji)
                    await ctx.send(f"Reaction role for {role} using {emoji} setted up! https://discord.com/channels/{ctx.message.guild.id}/{msg.channel.id}/{msg.id}")

        else:
            try:
                pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX
            await ctx.send(f"Looks like you forgot something, make sure to follow this format when setting up reaction role\n```{pref}rr <messageid> <role> <emoji>```\nFor the role part, you can either mention the role or use it's id")

            
    @commands.command(aliases=['removereactionrole', 'rrremove', 'reactionroleremove'])
    @commands.has_permissions(administrator=True)
    async def removerr(self, ctx, msg:discord.Message=None, emoji=None):

        if msg and emoji is not None:
            guildrr = var.REACTIONROLES.find_one({"_id": ctx.guild.id})

            def rr_exists():
                try:
                    for i in guildrr["reaction_roles"]:
                        if msg.id == i.get("messageid") and str(emoji) == i.get("emoji"):
                            return True
                        return False
                except AttributeError:
                    return False

            if rr_exists() == False:
                await ctx.send("This reaction role does not exist")
            else:
                rrlist = guildrr["reaction_roles"]
                newlist = rrlist.copy()
                for rrpairs in newlist:
                    if  msg.id == rrpairs.get("messageid") and str(emoji) == rrpairs.get("emoji"):
                        removethis = rrpairs
                
                newlist.remove(removethis)
                newdata = {"$set":{
                    "reaction_roles": newlist
                }}
                var.REACTIONROLES.update_one(guildrr, newdata)
                await msg.clear_reactions()
                await ctx.send(embed=discord.Embed(title="Reaction role removed", 
                description=f"Reaction role with {emoji} on [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id}) was removed",
                color=var.CGREEN))
        else:
            try:
                pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX

            await ctx.send(f"Looks like you missed out something, make sure to follow this format```{pref}removerr <messageid> <emoji>```")
            

    @commands.command(aliases=['listrr', 'rrall', 'rrlist', 'allreactionroles', 'listreactionroles'])
    @commands.has_permissions(administrator=True)
    async def allrr(self, ctx):

        embed = discord.Embed(title="All active reaction roles", color=var.CMAIN)
        guildrr = var.REACTIONROLES.find_one({"_id": ctx.guild.id})

        if guildrr is not None:
            for i in guildrr["reaction_roles"]:
                guild = self.bot.get_guild(ctx.guild.id)
                msg = await ctx.fetch_message(i.get("messageid"))
                role = guild.get_role(i.get("roleid"))
                emoji = i.get("emoji")
                embed.add_field(name=f"** **", value=f"{emoji} for {role.mention}\n [Jump to the message!](https://discord.com/channels/{guild.id}/{msg.channel.id}/{msg.id})", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have any active reaction roles right now")
    

    @commands.command(aliases=["rrunique", "addunique", "markunique", "uniquemark", "msgunique", "uniquereact", "uniquereactions"])
    @commands.has_permissions(administrator=True)
    async def uniquerr(self, ctx, msg:discord.Message=None):
        
        if msg is not None:
            guildrr = var.REACTIONROLES.find_one({"_id": ctx.guild.id})
            if guildrr is not None:
                allmsgids = []
                uniquelist = guildrr["unique_messages"]
                for i in guildrr["reaction_roles"]:
                    allmsgids.append(i.get("messageid"))
                    
                if msg.id in allmsgids:
                    newlist = uniquelist.copy()
                    
                    newlist.append(msg.id)
                    newdata = {"$set":{
                        "unique_messages": newlist
                    }}
                    var.REACTIONROLES.update_one(guildrr, newdata)
                    await ctx.send(embed=discord.Embed(title="Successfully marked the message with unique reactions", 
                    description=f"Now users can only react to one emoji and take one role in [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id})",
                    color=var.CGREEN))
                
                else:
                    await ctx.send("Hmm it looks like that the message id you entered does not have any reaction role.")
            else:
                await ctx.send("Cannot mark that message with unique reactions since you don't have any reaction roles yet :(")
        else:
            try:
                pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX
            await ctx.send(f"You need to enter your message id to make it unique too! Follow this format```{pref}uniquerr <messageid>")


    @commands.command(aliases=["removerrunique", "uniqueremove", "unmarkunique", "uniqueunmark", "rurr", "clearunique"])
    @commands.has_permissions(administrator=True)
    async def removeunique(self, ctx, msg:discord.Message=None):
        
        if msg is not None:
            guildrr = var.REACTIONROLES.find_one({"_id": ctx.guild.id})
            if guildrr is not None:
                allmsgids = []
                uniquelist = guildrr["unique_messages"]
                for i in guildrr["reaction_roles"]:
                    allmsgids.append(i.get("messageid"))
                    
                if msg.id in allmsgids and msg.id in uniquelist:
                    newlist = uniquelist.copy()
                    
                    newlist.remove(msg.id)
                    newdata = {"$set":{
                        "unique_messages": newlist
                    }}
                    var.REACTIONROLES.update_one(guildrr, newdata)
                    await ctx.send(embed=discord.Embed(title="Successfully unmarked the message with unique reactions", 
                    description=f"Now users can react and take multiple roles in [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id})",
                    color=var.CGREEN))
                
                else:
                    await ctx.send("Hmm it looks like that the message id you entered does not have any reaction role so can't remove the unique mark either.")
            else:
                await ctx.send("Cannot remove the unique mark from that message since you don't have any reaction roles yet :(")
        else:
            try:
                pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX
            await ctx.send(f"You need to enter your message id to make it unique too! Follow this format```{pref}uniquerr <messageid>")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guildrr = var.REACTIONROLES.find_one({"_id": payload.guild_id})
        
        if guildrr is not None and guildrr["reaction_roles"] is not None:           
            for i in guildrr["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(payload.emoji) == i.get("emoji"):
                    roleid = i.get("roleid")
                    
                    guild = self.bot.get_guild(payload.guild_id)
                    assignrole = guild.get_role(roleid)
                    if payload.member.bot == False:
                        await payload.member.add_roles(assignrole)

        if guildrr is not None and payload.message_id in guildrr["unique_messages"]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                    await message.remove_reaction(r.emoji, payload.member)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        guildrr = var.REACTIONROLES.find_one({"_id": payload.guild_id})
        if guildrr is not None and guildrr["reaction_roles"] is not None:
            for i in guildrr["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(payload.emoji) == i.get("emoji"):
                    roleid = i.get("roleid")

                    member = await(await self.bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
                    if member is not None:
                        guild = self.bot.get_guild(payload.guild_id)
                        removerole = guild.get_role(roleid)
                        await member.remove_roles(removerole)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))

    