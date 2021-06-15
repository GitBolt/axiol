import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix
import asyncio


def levelhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Ah yes leveling, MEE6 who?", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"rank `<user>`", value="Shows server rank of the user, user ID or user mention can be used to check ranks, user field is optional for checking rank of yourself.", inline=False
    ).add_field(name=getprefix(ctx)+"leaderboard", value="Shows server leaderboard!", inline=False
    ).add_field(name=getprefix(ctx)+"levelchart `<amount>`", value="Shows a Bar chart of the top users! Amount field is optional since 10 users are shown by default, max amount is 30", inline=False
    ).add_field(name=getprefix(ctx)+"givexp `<user>` `<amount>`", value="Gives user more XP! For user either user can be mentioned or ID can be used", inline=False
    ).add_field(name=getprefix(ctx)+"removexp `<user>` `<amount>`", value="Removes user more XP! For user either user can be mentioned or ID can be used", inline=False
    #).add_field(name=getprefix(ctx)+"award", value="Setup awards for reaching certain amount of xp!", inline=False
    ).add_field(name=getprefix(ctx)+"levelinfo", value="Shows the server's leveling settings!", inline=False
    ).add_field(name=getprefix(ctx)+"levelconfig", value=f"Configure leveling settings!", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def modhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="What's better than entering a sweet little ban command?", description="For all fields which require `user`, either the User ID or User Mention can be used. Reason everywhere is optional :ok_hand:", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"ban `<user>` `<reason>`", value="Bans a user from the server", inline=False
    ).add_field(name=getprefix(ctx)+"unban `<user>`", value="Unbans a any already banned user", inline=False
    ).add_field(name=getprefix(ctx)+"kick `<reason>`", value="Kicks the user out of the server", inline=False
    ).add_field(name=getprefix(ctx)+"mute", value="Disables the ability for users to send text messages in all channels! Permissions can be changed", inline=False
    ).add_field(name=getprefix(ctx)+"unmute", value="Removes the 'Muted' role therefore lets the user send messages", inline=False
    ).add_field(name=getprefix(ctx)+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False
    ).add_field(name=getprefix(ctx)+"nick `<member>`", value="Changes nickname of a member", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def rrhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Reaction Roles", description="For roles either the Role ID (to not disturb users in case they have the role) or Role mention can be used", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"rr `<#channel>` `<messageid>` `<role>` `<emoji>`", value="Setup reaction roles in your server!", inline=False
    ).add_field(name=getprefix(ctx)+"removerr `<messageid>` `<emoji>`", value="Remove any existing reaction role", inline=False
    ).add_field(name=getprefix(ctx)+"allrr", value="View all active reaction roles in the server!", inline=False
    ).add_field(name=getprefix(ctx)+"uniquerr `<messageid>`", value="Mark a message with unique reactions! Users would be able to react once hence take one role from the message", inline=False
    ).add_field(name=getprefix(ctx)+"removeunique `<messageid>`", value="Unmark the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
    return embed

def welcomehelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Welcome Greetings", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"welcomecard", value="See your server's welcome card!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomechannel `<#channel>`", value="Change welcome channel!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomemessage", value="Change welcome message!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomegreeting", value="Change welcome greeting!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomeimage", value="Change the welcome image!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomerole `<role>`", value="Assign automatic role to a member when they join! For role either role mention or id can be used", inline=False
    ).add_field(name=getprefix(ctx)+"welcomereset", value="Reset to the default welcome embed message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def verifyhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Verification", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"verifyinfo", value="Get information current server verification setup!", inline=False
    ).add_field(name=getprefix(ctx)+"verifychannel `<#channel>`", value="Change the verification channel!", inline=False
    ).add_field(name=getprefix(ctx)+"verifyswitch", value="Switch between verification type", inline=False
    ).add_field(name=getprefix(ctx)+"verifyrole `<role>`", value="Give a role to users when they successfully verify!", inline=False
    ).add_field(name=getprefix(ctx)+"verifyroleremove `<role>`", value="Remove a verified role if setted up", inline=False
    ).add_field(name=getprefix(ctx)+"verifyremove", value="Remove verification from your server (Removes data and disables the plugin)", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
    ).set_footer(text="For verify role, you can only set one at a time, if a verify role is already setted up then setting up another one will replace the existing one")
    return embed

def chatbothelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Chatbot", color=var.C_MAIN,
    description="I will reply to pings in every channel however setting up a bot chat channel won't require you ping me!"
    ).add_field(name=getprefix(ctx)+"setchatbot `<#channel>`", value="Make a channel for chatting with me! All messages sent there will be replied by me :D", inline=False
    ).add_field(name=getprefix(ctx)+"removechatbot `<#channel>`", value="Remove a chatbot channel (if added)", inline=False
    ).add_field(name=getprefix(ctx)+"chatbotchannels", value="View all channels where chat bot is enabled!", inline=False
    ).add_field(name=getprefix(ctx)+"chatbotreport `<description>`", value="Send any report/bug related to the chatbot directly to the [Support server](https://discord.gg/KTn4TgwkUT)!"
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def musicbothelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Music", color=var.C_MAIN,
    description="🎧 Let's vibe to some music! For Voice Channels either their Name or ID can be used since they can't be mentioned using `#` like Text Channels"
    ).add_field(name=getprefix(ctx)+"connect `<voicechannel>`", value="Joins a voice channel! Voice Channel field is optional if you want me to join the same VC inside which you are in :D", 
    ).add_field(name=getprefix(ctx)+"play `<search>`", value="Search for music to play on YouTube! You can also use the video URL",inline=False 
    ).add_field(name=getprefix(ctx)+"pause", value="Pauses the currently playing music", inline=False 
    ).add_field(name=getprefix(ctx)+"resume", value="Resumes the paused music", inline=False 
    ).add_field(name=getprefix(ctx)+"np", value="Shows the current playing song, NP is short for Now Playing!",inline=False
    ).add_field(name=getprefix(ctx)+"queue", value="Shows all the upcoming songs in the queue!",inline=False 
    ).add_field(name=getprefix(ctx)+"remove `<position>`", value=f"Removes a song from it's given queue position!", 
    ).add_field(name=getprefix(ctx)+"skip", value="Skips the currently playing song", 
    ).add_field(name=getprefix(ctx)+"volume `<1-100 value>`", value="Change the music volume! The limit is from 0 to 100",
    ).add_field(name=getprefix(ctx)+"leave", value="Stops playing the music and leaves the VC",inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def extrahelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Extras", description="Commands that are useful but don't belong to other categories!", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"embed `<#channel>`",value="Generate an embed!", inline=False
    ).add_field(name=getprefix(ctx)+"stats", value="Shows server statistics!", inline=False
    ).add_field(name=getprefix(ctx)+"about", value="Information about me :sunglasses:", inline=False
    ).add_field(name=getprefix(ctx)+"suggest `<youridea>`",value="Suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)!", inline=False
    ).add_field(name=getprefix(ctx)+"invite",value="My bot invite link!", inline=False
    ).add_field(name=getprefix(ctx)+"source", value="Link to my Github repository since I am open source :D", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})

        embed = discord.Embed(
        title="Axiol Help",
        description=f"Help commands for the plugins which are enabled!",
        color=var.C_MAIN
        ).add_field(name=getprefix(ctx)+"prefix", value="Change prefix", inline=False
        ).add_field(name=getprefix(ctx)+"plugins", value=f"Configure plugins {var.E_PLUGINS}", inline=False
        ).set_footer(text="Either use the subcommand or react to the emojis below"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")

        for i in GuildDoc:
            if GuildDoc.get(i) == True:
                helpname = i.lower()
                if i.lower() == "reaction roles": #Reaction roles command doesn't have space in between reaction and roles
                    helpname = i.lower().replace(" ", "")
                embed.add_field(name=f"{getprefix(ctx)}help {helpname}", value=f"{i} Help {var.DICT_PLUGINEMOJIS.get(i)}", inline=False)

        embed.add_field(name=f"{getprefix(ctx)}help extras", value=f"Non plugin commands {var.E_CONTINUE}️ ", inline=False)
        helpmsg = await ctx.send(embed=embed)


        await helpmsg.add_reaction(var.E_PLUGINS)
        for i in GuildDoc:
            if GuildDoc.get(i) == True:
                await helpmsg.add_reaction(var.DICT_PLUGINEMOJIS.get(i))
        await helpmsg.add_reaction(var.E_CONTINUE)

        def check(reaction, user):
            return user == ctx.author and reaction.message == helpmsg


        HelpDict = {
            "Leveling": levelhelp,
            "Moderation": modhelp,
            "Reaction Roles":rrhelp,
            "Welcome": welcomehelp,
            "Verification": verifyhelp,
            "Chatbot": chatbothelp,
            "Music": musicbothelp
        }

        try:
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
                if str(reaction.emoji) in var.DICT_PLUGINEMOJIS.values():

                    helptype = list(var.DICT_PLUGINEMOJIS.keys())[list(var.DICT_PLUGINEMOJIS.values()).index(str(reaction.emoji))]
                    await helpmsg.edit(embed=HelpDict.get(helptype)(ctx))
                    try:
                        await helpmsg.remove_reaction(str(reaction.emoji), ctx.author)
                    except discord.Forbidden:
                        pass
                
                #Since extra help and plugin is always there
                if str(reaction.emoji) == var.E_CONTINUE:
                    await helpmsg.edit(embed=extrahelp(ctx))
                    try:
                        await helpmsg.remove_reaction(var.E_CONTINUE, ctx.author)
                    except discord.Forbidden:
                        pass
                if str(reaction.emoji) == var.E_PLUGINS:
                    try:
                        await helpmsg.clear_reactions()
                    except discord.Forbidden:
                        pass
                    await ctx.invoke(self.bot.get_command('plugins'))

        except asyncio.TimeoutError:
            try:
                await helpmsg.clear_reactions()
            except discord.Forbidden:
                await helpmsg.add_reaction(var.E_PLUGINS)
                for i in GuildDoc:
                    if GuildDoc.get(i) == True:
                        await helpmsg.remove_reaction(var.DICT_PLUGINEMOJIS.get(i), self.bot.user)
                await helpmsg.add_reaction(var.E_CONTINUE)


           
    @help.command()
    async def leveling(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Leveling") == True:
            await ctx.send(embed=levelhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Leveling plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def moderation(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Moderation") == True:
            await ctx.send(embed=modhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def reactionroles(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Reaction Roles") == True:
            await ctx.send(embed=rrhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Reaction Roles plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def welcome(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome") == True:
            await ctx.send(embed=welcomehelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def verification(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification") == True:
            await ctx.send(embed=verifyhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Verification plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def chatbot(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot") == True:
            await ctx.send(embed=chatbothelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Chatbot plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def music(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Music") == True:
            await ctx.send(embed=musicbothelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Music plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def extras(self, ctx):
        await ctx.send(embed=extrahelp(ctx))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelconfig(self, ctx):
        
        embed = discord.Embed(title="Configure leveling for this server",
        color=var.C_TEAL
        ).add_field(name=getprefix(ctx)+"xprange `<leastamount>` `<highestamount>`",value="Set the range between which users will be awarded with random xp", inline=False
        ).add_field(name=getprefix(ctx)+"blacklist `<#channel>`",value=f"Add the channel where you don't want users to gain xp.", inline=False
        ).add_field(name=getprefix(ctx)+"whitelist `<#channel>`",value=f"Whitelist an xp blacklisted channel.", inline=False
        ).add_field(name=getprefix(ctx)+"alertchannel `<#channel>`", value="Define the channel where alerts will be sent for level ups!", inline=False
        ).add_field(name=getprefix(ctx)+"togglealerts", value="Disable or Enable alert message for level ups!", inline=False
        ).add_field(name="Reset data", value=f"React to {var.E_DECLINE}", inline=False
        ).set_footer(text=f"Leveling is a plugin so to disable it, use the command {getprefix(ctx)}plugins and click on the leveling emoji")
        #).add_field(name=getprefix(ctx)+"maxlevel `<amount>`", value="Define the max level which can be achieved by a user", inline=False
        #).add_field(name=getprefix(ctx)+"alertmessage `<message>`", value=f"Change the alert message! Use these values in between:\n[user] [xp] [level]\n Make sure to put them between square brackets!", inline=False
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_DECLINE)

        def reactioncheck(reaction, user):
            if str(reaction.emoji) == var.E_DECLINE:
                return user == ctx.author and reaction.message == botmsg

        await self.bot.wait_for('reaction_add', check=reactioncheck)
        try:
            await botmsg.clear_reactions()
        except discord.Forbidden:
            pass
        embed = discord.Embed(
                    title="Rank data deletion",
                    description=f"Keep in mind that this action is irreversable",
                    color=var.C_ORANGE
        ).add_field(name="Confirm Delete", value=var.E_ACCEPT
        ).add_field(name="Cancel", value=var.E_DECLINE
        )
        botdeletemsg = await ctx.send(embed=embed)
        await botdeletemsg.add_reaction(var.E_ACCEPT)
        await botdeletemsg.add_reaction(var.E_DECLINE)

        def deletereaction_check(reaction, user):
            return user == ctx.author and reaction.message == botdeletemsg
        
        reaction, user = await self.bot.wait_for('reaction_add', check=deletereaction_check, timeout=60.0)
        if str(reaction.emoji) == var.E_ACCEPT:
            db.LEVELDATABASE.get_collection(str(ctx.guild.id)).remove({ "_id" : { "$ne": 0 } })
            await ctx.send(embed=discord.Embed(
                        title="Leveling removed", 
                        description="Leveling have been removed from this server, that means all the rank data has been deleted", 
                        color=var.C_ORANGE)
                        )
        if str(reaction.emoji) == var.E_DECLINE:
            await ctx.send("Woosh that was close, cancelled leveling data deletion.")


def setup(bot):
    bot.add_cog(Help(bot))
