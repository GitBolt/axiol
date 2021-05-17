import discord
from discord.ext import commands
from utils.vars import DEFAULT_PREFIX, MONGOCLIENT

DATABASE = MONGOCLIENT['Axiol']
PREFIXES = DATABASE["Prefixes"] #Prefixes Collection
REACTIONROLES = DATABASE["ReactionRoles"] #ReactionRoles Collection

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def rr(self, ctx, msg:discord.Message=None, role: discord.Role=None, emoji=None):

        if msg is not None and role is not None and emoji is not None:
            if REACTIONROLES.find_one({"messageid": msg.id, "emoji": emoji}) == None:
                REACTIONROLES.insert_one({"_id": REACTIONROLES.estimated_document_count()+1, "serverid": ctx.author.guild.id, "messageid": msg.id, "roleid": role.id, "emoji": str(emoji)})
                await msg.add_reaction(emoji)
                await ctx.send(f"Reaction role for {role} using {emoji} setted up! https://discord.com/channels/{ctx.message.guild.id}/{msg.channel.id}/{msg.id}")
            else:
                await ctx.send(f"You have already setted up this reaction role using {emoji} haha, I can see it in the database!")
        else:
            try:
                pref = PREFIXES.find_one({"serverid": ctx.author.guild.id}).get("prefix")
            except AttributeError:
                pref = DEFAULT_PREFIX
            await ctx.send(f"Looks like you forgot something, make sure to follow this format when setting up reaction role ```{pref}rr <messageid> <role> <emoji>``` For the role part, you can either mention the role or use it's id")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reactionrolecheck = REACTIONROLES.find_one({"serverid": payload.guild_id, "messageid": payload.message_id, "emoji": str(payload.emoji)})
        if reactionrolecheck != None:
            guild = self.bot.get_guild(reactionrolecheck.get("serverid"))
            assignrole = guild.get_role(reactionrolecheck.get("roleid"))
            
            await payload.member.add_roles(assignrole)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reactionrolecheck = REACTIONROLES.find_one({"serverid": payload.guild_id, "messageid": payload.message_id, "emoji": str(payload.emoji)})
        if reactionrolecheck is not None:
            member = await(await self.bot.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            if member is not None:
                guild = self.bot.get_guild(reactionrolecheck.get("serverid"))
                removerole = guild.get_role(reactionrolecheck.get("roleid"))
                
                await member.remove_roles(removerole)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))

    