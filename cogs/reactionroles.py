import discord
from discord.ext import commands
import utils.vars as var

DATABASE = var.MONGOCLIENT['Axiol']
PREFIXES = DATABASE["Prefixes"] #Prefixes Collection
REACTIONROLES = DATABASE["ReactionRoles"] #ReactionRoles Collection

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['reactionrole', 'addrr', 'addreactionrole', 'rradd', 'reactionroleadd'])
    @commands.has_permissions(administrator=True)
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
                pref = var.DEFAULT_PREFIX
            await ctx.send(f"Looks like you forgot something, make sure to follow this format when setting up reaction role ```{pref}rr <messageid> <role> <emoji>``` For the role part, you can either mention the role or use it's id")


    @commands.command(aliases=['removereactionrole', 'rrremove', 'reactionroleremove'])
    @commands.has_permissions(administrator=True)
    async def removerr(self, ctx, msg:discord.Message=None, emoji=None):
        if msg is not None and emoji is not None:
            if REACTIONROLES.find_one({"messageid": msg.id, "emoji": str(emoji)}) == None:
                await ctx.send("This reaction role doesn't even exist")
            else:
                deleterr = REACTIONROLES.find_one({"messageid": msg.id, "emoji": str(emoji)})
                REACTIONROLES.delete_one(deleterr)
                await msg.clear_reactions()
                await ctx.send(embed=discord.Embed(title="Reaction role removed", 
                description=f"Reaction role with {emoji} on [this message](https://discord.com/channels/{ctx.author.guild.id}/{msg.channel.id}/{msg.id}) was removed",
                color=var.GREEN))
        else:
            try:
                pref = PREFIXES.find_one({"serverid": ctx.author.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX

            await ctx.send(f"Looks like you missed out something, make sure to follow this format```{pref}removerr <messageid> <emoji>```")

    @commands.command(aliases=['listrr', 'rrall', 'rrlist', 'allreactionroles', 'listreactionroles'])
    @commands.has_permissions(administrator=True)
    async def allrr(self, ctx):
        embed = discord.Embed(title="All active reaction roles", color=var.MAGENTA)
        guildrr = REACTIONROLES.find({"serverid": ctx.author.guild.id})

        if REACTIONROLES.find_one({"serverid": ctx.author.guild.id}) is not None:
            for i in guildrr:
                guild = self.bot.get_guild(ctx.author.guild.id)
                msg = await ctx.fetch_message(i.get("messageid"))
                role = guild.get_role(i.get("roleid"))
                emoji = i.get("emoji")

                embed.add_field(name=f"** **", value=f"{emoji} for {role.mention}\n [Jump to the message!](https://discord.com/channels/{guild.id}/{msg.channel.id}/{msg.id})", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have any active reaction roles right now")
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reactionrolecheck = REACTIONROLES.find_one({"serverid": payload.guild_id, "messageid": payload.message_id, "emoji": str(payload.emoji)})
        if reactionrolecheck != None:
            if payload.member.bot is not True:
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

    