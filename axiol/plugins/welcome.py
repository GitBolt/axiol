import asyncio
import disnake
from disnake.ext import commands
import constants as var
import database as db
from functions import get_prefix
from constants import greeting
from ext.permissions import has_command_permission


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled"""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if guild_doc.get("Welcome"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Welcome plugin is "
                        f"disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @commands.command(name="welcomesetup")
    @has_command_permission()
    async def welcome_setup(self, ctx):
        """This command isn't really used.
        just put this here to invoke on first welcome plugin enable
        """
        await ctx.send(
            "Now send the channel where you want me to send welcome message."
        )

        def message_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        user_msg = await self.bot.wait_for("message", check=message_check)

        try:
            channel_id = int(user_msg.content.strip("<>#"))

        except Exception:
            await db.PLUGINS.update_one(
                db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set": {"Welcome": False}}
            )

            return await ctx.send(
                embed=disnake.Embed(
                    title="Invalid Channel",
                    description=(
                        "🚫 I was not able to find the channel which you"
                        " entered. The plugin has been disabled, try again"
                    ),
                    color=var.C_RED,
                ).set_footer(
                    text=(
                        "You can either mention the channel (example: #general)"
                        " or use the channel's id (example: 843516084266729515)"
                    )
                )
            )

        await db.WELCOME.insert_one(
            {
                "_id": ctx.guild.id,
                "channelid": channel_id,
                "message": None,
                "greeting": "Hope you enjoy your stay here ✨",
                "image": (
                    "https://cdn.disnakeapp.com/attachments/"
                    "843519647055609856/864924991597314078/Frame_1.png"
                ),
                "assignroles": [],
            }
        )

        success_embed = disnake.Embed(
            title="Welcome greeting successfully setup",
            description=(
                f"{var.E_ACCEPT} New members will now be greeted in"
                f" {self.bot.get_channel(channel_id).mention}!"
            ),
            color=var.C_GREEN,
        ).add_field(
            name="To configure further", value=f"`{await get_prefix(ctx)}help welcome`"
        )

        await ctx.send(embed=success_embed)

    @commands.command(name="wcard")
    @has_command_permission()
    async def w_card(self, ctx):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        def get_content():
            if guild_doc.get("message") is None:
                content = greeting(ctx.author.mention)
            else:
                content = guild_doc.get("message")
            return content

        embed = disnake.Embed(
            title="Welcome to the server!",
            description=guild_doc.get("greeting"),
            color=disnake.Colour.random(),
        ).set_image(url=guild_doc.get("image"))

        await ctx.send(content=get_content(), embed=embed)

    @commands.command(name="wchannel")
    @has_command_permission()
    async def w_channel(self, ctx, channel: disnake.TextChannel = None):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        if channel is not None:
            new_data = {"$set": {"channelid": channel.id}}

            await db.WELCOME.update_one(guild_doc, new_data)

            await ctx.send(
                embed=disnake.Embed(
                    title="Changed welcome channel",
                    description=(
                        f"{var.E_ACCEPT} Now users will be"
                        f" greeted in {channel.mention}"
                    ),
                    color=var.C_GREEN,
                )
            )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the greeting channel to change it"
                    ),
                    color=var.C_RED,
                ).add_field(
                    name="Format", value=f"`{await get_prefix(ctx)}wchannel <#channel>`"
                )
            )

    @commands.command(name="wmessage")
    @has_command_permission()
    async def w_message(self, ctx):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(
            embed=disnake.Embed(
                tite="Send a message to make it the welcome message",
                description=(
                    "The next message which"
                    " you will send will become the embed message!"
                ),
                color=var.C_BLUE,
            )
            .add_field(name="Cancel", value=f"Type `cancel` to stop this process")
            .set_footer(
                text=(
                    "Don't confuse this with welcome greeting, that's different"
                    "! This is the text message which pings the member and is"
                    " outside the embed card itself, the greeting is the "
                    "description of the embed"
                )
            )
        )

        def msg_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            user_msg = await self.bot.wait_for(
                "message", check=msg_check, timeout=300.0
            )

            if user_msg.content == "cancel" or user_msg.content == "`cancel`":
                await ctx.send("Cancelled welcome message change :ok_hand:")

            else:
                new_data = {"$set": {"message": user_msg.content}}

                await db.WELCOME.update_one(guild_doc, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        title=(
                            f"{var.E_ACCEPT}"
                            " Successfully changed the welcome message!"
                        ),
                        description=(
                            f"The new welcome message is:\n" f"**{user_msg.content}**"
                        ),
                        color=var.C_GREEN,
                    )
                )
        except asyncio.TimeoutError:
            await ctx.send(
                f"**{ctx.author.name}** you took too long"
                f" to enter your message, try again maybe?"
            )

    @commands.command(name="wgreeting")
    @has_command_permission()
    async def w_greeting(self, ctx):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(
            embed=disnake.Embed(
                tite="Send a message to make it the welcome greeting!",
                description=(
                    "The next message which you will send "
                    "will become the embed description!"
                ),
                color=var.C_BLUE,
            )
            .add_field(name="Cancel", value=f"Type `cancel` to cancel this")
            .set_footer(
                text=(
                    "Don't confuse this with embed message, that's different!"
                    " This is the embed description which is inside the embed"
                    " itself however welcome message is the content outside"
                    " where members are pinged!"
                )
            )
        )

        def msg_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            user_msg = await self.bot.wait_for("message", check=msg_check, timeout=60.0)

            if user_msg.content == "cancel" or user_msg.content == "`cancel`":
                await ctx.send("Cancelled welcome message change :ok_hand:")

            else:
                new_data = {"$set": {"welcomegreeting": user_msg.content}}

                await db.WELCOME.update_one(guild_doc, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        title=(
                            f"{var.E_ACCEPT} Successfully changed "
                            f"the greeting message!"
                        ),
                        description=(
                            f"The new greeting message is:\n" f"**{user_msg.content}**"
                        ),
                        color=var.C_GREEN,
                    )
                )
        except asyncio.TimeoutError:
            await ctx.send(
                f"**{ctx.author.name}** you took too long"
                f" to enter your message, try again maybe?"
            )

    @commands.command(name="wimage")
    @has_command_permission()
    async def w_image(self, ctx):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(
            embed=disnake.Embed(
                tite="Send a message to make it the image",
                description="Either send the image as a file or use a link!",
                color=var.C_BLUE,
            ).add_field(name="Cancel", value=f"Type `cancel` to cancel this")
        )

        def msg_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            user_msg = await self.bot.wait_for("message", check=msg_check, timeout=60.0)

            if user_msg.content == "cancel" or user_msg.content == "`cancel`":
                await ctx.send("Cancelled image change :ok_hand:")

            if user_msg.attachments:
                new_data = {"$set": {"image": user_msg.attachments[0].url}}

                await db.WELCOME.update_one(guild_doc, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        title=f"{var.E_ACCEPT} Successfully changed welcome image",
                        description="New welcome image is:",
                        color=var.C_GREEN,
                    ).set_image(url=user_msg.attachments[0].url)
                )

            elif user_msg.content.startswith("http"):
                new_data = {"$set": {"image": user_msg.content}}

                await db.WELCOME.update_one(guild_doc, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        title=(f"{var.E_ACCEPT} Successfully changed welcome image"),
                        description="New welcome image is:",
                        color=var.C_GREEN,
                    ).set_image(url=user_msg.content)
                )

            else:
                await ctx.send("Invalid image, try again")

        except asyncio.TimeoutError:
            await ctx.send(
                f"**{ctx.author.name}** you took too long to enter "
                f"your welcome image, try again maybe?"
            )

    @commands.command(name="wrole")
    @has_command_permission()
    async def w_role(self, ctx, role: disnake.Role = None):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})

        if role is not None:
            role_list = guild_doc.get("assignroles")
            updated_list = role_list.copy()
            updated_list.append(role.id)

            new_data = {"$set": {"assignroles": updated_list}}

            await db.WELCOME.update_one(guild_doc, new_data)

            await ctx.send(
                embed=disnake.Embed(
                    title="Successfully added auto assign role",
                    description=(
                        f"{var.E_ACCEPT} Users will be automatically "
                        f"given {role.mention} when they join"
                    ),
                    color=var.C_GREEN,
                )
            )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description="🚫 You need to define the role", color=var.C_RED
                )
                .add_field(
                    name="Format", value=f"`{await get_prefix(ctx)}wrole <role>`"
                )
                .set_footer(text="For role either role ID or role mention can be used")
            )

    @commands.command(name="wbots")
    @has_command_permission()
    async def w_bots(self, ctx):
        data = await db.WELCOME.find_one({"_id": ctx.guild.id})
        embed = disnake.Embed(title="Greet bots")
        if data["greet_bots"]:
            embed.description = (
                f"Currently, bots are greeted by me when they join.\n"
                f"React to the {var.E_DISABLE} emoji "
                f"to disable me greeting them."
            )

            embed.color = var.C_GREEN

        else:
            embed.description = (
                f"Currently, bots are not greeted by me when they join.\n"
                f" React to  the {var.E_ENABLE} emoji "
                f"to enable me greeting them."
            )

            embed.color = var.C_RED

        bot_msg = await ctx.send(embed=embed)

        await bot_msg.add_reaction(
            var.E_DISABLE if data["greet_bots"] else var.E_ENABLE
        )

        def check(reaction, user):
            if str(reaction.emoji) in [var.E_DISABLE, var.E_ENABLE]:
                return user == ctx.author and reaction.message == bot_msg

        await self.bot.wait_for("reaction_add", check=check, timeout=60)
        new_data = {"$set": {"greet_bots": False if data["greet_bots"] else True}}

        await db.WELCOME.update_one(data, new_data)

        try:
            await bot_msg.clear_reactions()

        except disnake.Forbidden:
            pass

        embed.description = (
            "Bots won't be greeted from now by me."
            if data["greet_bots"]
            else "Bots would be greeted from now by me."
        )

        embed.color = var.C_RED if data["greet_bots"] else var.C_GREEN
        await bot_msg.edit(embed=embed)

    @commands.command(name="wreset")
    @has_command_permission()
    async def w_reset(self, ctx):
        guild_doc = await db.WELCOME.find_one({"_id": ctx.guild.id})
        new_data = {
            "$set": {
                "message": None,
                "welcomegreeting": "Hope you enjoy your stay here ✨",
                "image": (
                    "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                    "864924991597314078/Frame_1.png"
                ),
                "assignroles": [],
                "greet_bots": True,
            }
        }

        await db.WELCOME.update_one(guild_doc, new_data)
        await ctx.send(
            embed=disnake.Embed(
                description=(
                    f"{var.E_ACCEPT} Successfully changed the welcome embed"
                    f" back to the default one"
                ),
                color=var.C_GREEN,
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):

        welcome_guild_ids = [
            doc["_id"] async for doc in db.PLUGINS.find({"Welcome": True})
        ]
        welcome_doc = await db.WELCOME.find_one({"_id": member.guild.id})

        if (member.guild.id not in welcome_guild_ids) or (
            member.bot and not welcome_doc["greet_bots"]
        ):
            return

        channel = self.bot.get_channel(welcome_doc.get("channelid"))

        def get_content():
            if welcome_doc.get("message") is None:
                content = greeting(member.mention)
            else:
                content = f"{member.mention} {welcome_doc.get('message')}"

            return content

        embed = disnake.Embed(
            title="Welcome to the server!",
            description=welcome_doc.get("greeting"),
            color=disnake.Colour.random(),
        ).set_image(url=welcome_doc.get("image"))

        await channel.send(content=get_content(), embed=embed)

        auto_roles = welcome_doc["assignroles"]

        if auto_roles:
            for i in auto_roles:
                auto_role = member.guild.get_role(i)
                await member.add_roles(auto_role)


def setup(bot):
    bot.add_cog(Welcome(bot))
