import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix, reactionrolespagination

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Reaction Roles") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Reaction Roles plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @commands.command()
    async def rr(self, ctx, channel:discord.TextChannel=None, msgid:int=None, role: discord.Role=None, emoji=None):
        bot_member = ctx.guild.get_member(self.bot.user.id)
        try:
            botrole = bot_member.roles[1]
        except IndexError:
            botrole = bot_member.roles[0]
            
        if channel and msgid and role and emoji is not None:
            try:
                msg = await channel.fetch_message(msgid)
                if botrole.position > role.position:
                    GuildDoc = db.REACTIONROLES.find_one({"_id": ctx.guild.id})
                    if GuildDoc == None:
                        db.REACTIONROLES.insert_one({

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
                        guildrrlist = GuildDoc["reaction_roles"]
                        def check():
                            for i in guildrrlist: 
                                if i.get("messageid") == msg.id and i.get("emoji") == str(emoji):
                                    return True

                        if check() == True:
                            await ctx.send(f"You have already setted up this reaction role using {emoji} on that message :D I can see it in the database!")
                        else:
                            newlist = guildrrlist.copy()
                            newlist.append({"messageid":msg.id, "roleid": role.id, "emoji": str(emoji)})
                            newdata = {"$set":{
                                "reaction_roles": newlist
                            }}
                            db.REACTIONROLES.update_one(GuildDoc, newdata)
                            await msg.add_reaction(emoji)
                            await ctx.send(f"Reaction role for {role} using {emoji} setted up! https://discord.com/channels/{ctx.message.guild.id}/{msg.channel.id}/{msg.id}")
                else:
                    await ctx.send(embed=discord.Embed(
                        title="Role position error",
                        description=f"The role {role.mention} is above my role ({ botrole.mention}), in order for me to update any role (reaction roles) my role needs to be above that role, just move my role above your reaction role as shown below\n\n **Server Settings > Roles > Click on the {botrole.mention} Role > Drag it above the {role.mention} Role **(Shown as the Developer role in the image below)",
                        color=var.C_RED
                    ).set_image(url="https://cdn.discordapp.com/attachments/843519647055609856/850711272726986802/unknown.png")
                    )

            except:
                await ctx.send(embed=discord.Embed(
                            title="Invalid Message ID",
                            description=f"There are no messages with the ID **{msgid}** in {channel.mention}",
                            color=var.C_RED
                ))

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the channel, message, role and emoji all three to add a reaction role",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}rr <#channel> <messageid> <role> <emoji>`"
            ).set_footer(text="You can use either role ID or mention it (use ID if you don't want to disturb everyone having the role)")
            )


            
    @commands.command()
    async def removerr(self, ctx, msg:discord.Message=None, emoji:str=None):
        
        if msg and emoji is not None:
            GuildDoc = db.REACTIONROLES.find_one({"_id": ctx.guild.id})
            
            def rr_exists():
                try:
                    for i in GuildDoc["reaction_roles"]:
                        if i.get("messageid") == msg.id and i.get("emoji") == emoji:
                            return True
                except AttributeError:
                    return False

            if rr_exists():
                def getpair(lst):
                    for rrpairs in lst:
                        if  msg.id == rrpairs.get("messageid") and str(emoji) == rrpairs.get("emoji"):
                            return rrpairs

                rrlist = GuildDoc["reaction_roles"]
                newlist = rrlist.copy()

                newlist.remove(getpair(newlist))
                newdata = {"$set":{
                    "reaction_roles": newlist
                }}
                db.REACTIONROLES.update_one(GuildDoc, newdata)
                await msg.clear_reactions()
                await ctx.send(embed=discord.Embed(
                            title="Reaction role removed", 
                            description=f"Reaction role with {emoji} on [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id}) was removed",
                            color=var.C_GREEN)
                            )
            elif not rr_exists():
                await ctx.send("This reaction role does not exist")
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the message  and emoji both to remove a reaction role",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}removerr <messageid> <emoji>`"
            )
            )
        
        


    @commands.command(aliases=['rrall'])
    async def allrr(self, ctx):

        Guild = self.bot.get_guild(ctx.guild.id)
        GuildDoc = db.REACTIONROLES.find_one({"_id": Guild.id})
        if GuildDoc is not None:

            rramount = len(GuildDoc.get("reaction_roles"))
            if rramount <= 10:
                exactpages = 1
            else:
                exactpages = rramount / 10
            all_pages = round(exactpages)

            embed = discord.Embed(
            title="All active reaction roles", 
            color=var.C_MAIN
            )
            
            rrcount = 0
            for i in GuildDoc["reaction_roles"]:
                rrcount += 1
                messageid = i.get("messageid")
                role = Guild.get_role(i.get("roleid"))
                emoji = i.get("emoji")
                embed.add_field(name="** **", value=f"{emoji} for {role.mention} in message ID `{messageid}`", inline=False)
                if rrcount == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction("◀️")
            await botmsg.add_reaction("⬅️")
            await botmsg.add_reaction("➡️")
            await botmsg.add_reaction("▶️")

            def reactioncheck(reaction, user):
                if str(reaction.emoji) == "◀️" or str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡️" or str(reaction.emoji) == "▶️":
                    return user == ctx.author and reaction.message == botmsg
            
            current_page = 0
            while True:
                reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
                if str(reaction.emoji) == "◀️":
                    try:
                        await botmsg.remove_reaction("◀️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = 0
                    await reactionrolespagination(current_page, all_pages, embed, Guild, GuildDoc)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await botmsg.remove_reaction("➡️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page += 1
                    await reactionrolespagination(current_page, all_pages, embed, Guild, GuildDoc)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await botmsg.remove_reaction("⬅️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page -= 1
                    if current_page < 0:
                        current_page += 1
                    await reactionrolespagination(current_page, all_pages, embed, Guild, GuildDoc)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await botmsg.remove_reaction("▶️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = all_pages-1
                    await reactionrolespagination(current_page, all_pages, embed, Guild, GuildDoc)
                    await botmsg.edit(embed=embed)

        else:
            await ctx.send("This server does not have any active reaction roles right now")
    


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def uniquerr(self, ctx, msg:discord.Message=None):
        
        if msg is not None:
            GuildDoc = db.REACTIONROLES.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None:
                allmsgids = []
                uniquelist = GuildDoc["unique_messages"]
                for i in GuildDoc["reaction_roles"]:
                    allmsgids.append(i.get("messageid"))
                    
                if msg.id in allmsgids:
                    newlist = uniquelist.copy()
                    
                    newlist.append(msg.id)
                    newdata = {"$set":{
                        "unique_messages": newlist
                    }}
                    db.REACTIONROLES.update_one(GuildDoc, newdata)
                    await ctx.send(embed=discord.Embed(
                                title="Successfully marked the message with unique reactions", 
                                description=f"Now users can only react to one emoji and take one role in [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id})",
                                color=var.C_GREEN)
                                )
                
                else:
                    await ctx.send("Hmm it looks like that the message id you entered does not have any reaction role.")
            else:
                await ctx.send("Cannot mark that message with unique reactions since this server does not have any reaction roles yet :(")
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the message in order to mark it with unique reactions",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}uniquerr <messageid>`"
            )
            )



    @commands.command()
    async def removeunique(self, ctx, msg:discord.Message=None):
        
        if msg is not None:
            GuildDoc = db.REACTIONROLES.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None:
                allmsgids = []
                uniquelist = GuildDoc["unique_messages"]
                for i in GuildDoc["reaction_roles"]:
                    allmsgids.append(i.get("messageid"))
                    
                if msg.id in allmsgids and msg.id in uniquelist:
                    newlist = uniquelist.copy()
                    
                    newlist.remove(msg.id)
                    newdata = {"$set":{
                        "unique_messages": newlist
                    }}
                    db.REACTIONROLES.update_one(GuildDoc, newdata)
                    await ctx.send(embed=discord.Embed(
                                title="Successfully unmarked the message with unique reactions", 
                                description=f"Now users can react and take multiple roles in [this message](https://discord.com/channels/{ctx.guild.id}/{msg.channel.id}/{msg.id})",
                                color=var.C_GREEN)
                                )
                else:
                    await ctx.send("Hmm it looks like that the message id you entered does not have any reaction role so can't remove the unique mark either.")
            else:
                await ctx.send("Cannot remove the unique mark from that message since you don't have any reaction roles yet :(")
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the message in order to unmark it with unique reactions",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}uniquerr <messageid>`"
            )
            )



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #Listeners don't care about cog checks so need to add a check manually
        GuildDoc = db.REACTIONROLES.find_one({"_id": payload.guild_id})
        
        if GuildDoc is not None and GuildDoc["reaction_roles"] is not None:           
            for i in GuildDoc["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(payload.emoji) == i.get("emoji"):
                    roleid = i.get("roleid")
                    
                    guild = self.bot.get_guild(payload.guild_id)
                    assignrole = guild.get_role(roleid)
                    if payload.member.bot == False:
                        await payload.member.add_roles(assignrole)

        if GuildDoc is not None and payload.message_id in GuildDoc["unique_messages"]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                    await message.remove_reaction(r.emoji, payload.member)



    @commands.Cog.listener()
    #Listeners don't care about cog checks so need to add a check manually
    async def on_raw_reaction_remove(self, payload):

        GuildDoc = db.REACTIONROLES.find_one({"_id": payload.guild_id})
        if GuildDoc is not None and GuildDoc["reaction_roles"] is not None:
            for i in GuildDoc["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(payload.emoji) == i.get("emoji"):
                    roleid = i.get("roleid")

                    member = await(await self.bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
                    if member is not None:
                        guild = self.bot.get_guild(payload.guild_id)
                        removerole = guild.get_role(roleid)
                        await member.remove_roles(removerole)



def setup(bot):
    bot.add_cog(ReactionRoles(bot))

    
