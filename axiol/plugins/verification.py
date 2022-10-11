import random
import asyncio
import disnake
from disnake.ext import commands
import database as db
import constants as var
from functions import get_prefix
from ext.permissions import has_command_permission


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Verification"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Verification plugin"
                        " is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @commands.command(name="verifysetup")
    async def verify_setup(self, ctx):
        embed = disnake.Embed(
            title="Send the verify channel",
            description=(
                "Since this is the first time this plugin is being enabled, "
                "I need to know where I am supposed to verify new members :D"
            ),
            color=var.C_BLUE,
        ).set_footer(
            text=(
                "The next message which you will send will become the verify"
                " channel, make sure that the channel/channelID is valid other"
                " wise this won't work"
            )
        )

        bot_msg = await ctx.send(embed=embed)

        def message_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        user_msg = await self.bot.wait_for("message", check=message_check)

        try:
            ch = self.bot.get_channel(int(user_msg.content.strip("<>#")))

        except Exception:
            await db.PLUGINS.update_one(
                await db.PLUGINS.find_one({"_id": ctx.guild.id}),
                {"$set": {"Welcome": False}},
            )
            return await ctx.send(
                embed=disnake.Embed(
                    title="Invalid Channel",
                    description=(
                        "🚫 I was not able to find the channel which you entered"
                    ),
                    color=var.C_RED,
                ).set_footer(
                    text=(
                        "You can either mention the channel (example: #general)"
                        " or use the channel's id (example: 843516084266729515)"
                    )
                )
            )

        async def setup():
            try:
                n_verified = await ctx.guild.create_role(
                    name="Not Verified", colour=disnake.Colour(0xA8A8A8)
                )

                embed.title = "Processing..."
                embed.description = "Setting up everything, just a second"

                embed.set_footer(
                    text=(
                        "Creating the 'Not Verified' "
                        "role and setting up proper permissions"
                    )
                )

                await bot_msg.edit(embed=embed)

                try:
                    for i in ctx.guild.text_channels:
                        try:
                            await i.set_permissions(n_verified, view_channel=False)

                        except disnake.Forbidden:
                            await ctx.send(
                                embed=disnake.Embed(
                                    description=(
                                        f"Skipping {i.mention} since "
                                        f"I don't have access to that channel"
                                    ),
                                    color=var.C_ORANGE,
                                )
                            )

                    await ch.set_permissions(
                        n_verified, view_channel=True, read_message_history=True
                    )

                    await ch.set_permissions(self.bot.user, view_channel=True)

                    await ch.set_permissions(ctx.guild.default_role, view_channel=False)

                    await db.VERIFY.insert_one(
                        {
                            "_id": ctx.guild.id,
                            "type": "command",
                            "channel": ch.id,
                            "roleid": n_verified.id,
                            "assignrole": None,
                        }
                    )

                    success_embed = (
                        disnake.Embed(
                            title="Verification successfully setted up",
                            description=(
                                f"{var.E_ACCEPT} New members would need to "
                                f"verify in {ch.mention} to access other channels!"
                            ),
                            color=var.C_GREEN,
                        )
                        .add_field(
                            name="To configure further",
                            value=f"`{await get_prefix(ctx)}help verification`",
                        )
                        .set_footer(text="Default verification type is command")
                    )

                    await ctx.send(embed=success_embed)

                except disnake.Forbidden:
                    await db.PLUGINS.update_one(
                        await db.PLUGINS.find_one({"_id": ctx.guild.id}),
                        {"$set": {"Verification": False}},
                    )

                    await ctx.send(
                        embed=disnake.Embed(
                            title="Missing access",
                            description=(
                                "I don't have access or change role "
                                f"permissions in {ch.mention} to make it "
                                f"a verification channel"
                            ),
                            color=var.C_RED,
                        )
                    )

            except Exception:
                await db.PLUGINS.update_one(
                    await db.PLUGINS.find_one({"_id": ctx.guild.id}),
                    {"$set": {"Verification": False}},
                )

                await ctx.send(
                    embed=disnake.Embed(
                        title="Missing Permissions",
                        description=(
                            "🚫 I don't have permissions to create and "
                            "set permissions for roles"
                        ),
                        color=var.C_RED,
                    )
                )

        if disnake.utils.get(ctx.guild.roles, name="Not Verified"):
            alert_bot_msg = await ctx.send(
                embed=disnake.Embed(
                    title="**Not Verified** role found",
                    description=(
                        "I have found a role named 'Not Verified' in this "
                        "guild, do you want me to use this existing one or"
                        " let me create a new one with proper permissions?"
                    ),
                    color=var.C_BLUE,
                )
                .add_field(
                    name="Reuse",
                    value=(
                        f"{var.E_RECYCLE} Use the existing "
                        f"role without creating any new"
                    ),
                    inline=False,
                )
                .add_field(
                    name="Create",
                    value=(
                        f"{var.E_ACCEPT} Create a new one and use it "
                        f"while keeping the existing one"
                    ),
                    inline=False,
                )
                .add_field(
                    name="Update",
                    value=(
                        f"{var.E_CONTINUE} Replace a new one with the "
                        f"existing one (Hence deleting the existing one)",
                    ),
                    inline=False,
                )
            )

            await alert_bot_msg.add_reaction(var.E_RECYCLE)
            await alert_bot_msg.add_reaction(var.E_ACCEPT)
            await alert_bot_msg.add_reaction(var.E_CONTINUE)

            def alert_reaction_check(r, u):
                return u == ctx.author and r.message == alert_bot_msg

            reaction, user = await self.bot.wait_for(
                "reaction_add", check=alert_reaction_check
            )

            try:
                await alert_bot_msg.clear_reactions()

            except Exception:
                pass

            existing_n_verified = disnake.utils.get(
                ctx.guild.roles, name="Not Verified"
            )

            if str(reaction.emoji) == var.E_RECYCLE:
                await db.VERIFY.insert_one(
                    {
                        "_id": ctx.guild.id,
                        "type": "command",
                        "channel": ch.id,
                        "roleid": existing_n_verified.id,
                        "assignrole": None,
                    }
                )

                success_embed = (
                    disnake.Embed(
                        title="Verification successfully setup",
                        description=(
                            f"{var.E_ACCEPT} New members would need to verify "
                            f"in {ch.mention} to access other channels!"
                        ),
                        color=var.C_GREEN,
                    )
                    .add_field(
                        name="To configure further",
                        value=f"`{await get_prefix(ctx)}help verification`",
                    )
                    .set_footer(text="Default verification type is command")
                )

                await ctx.send(embed=success_embed)

            if str(reaction.emoji) == var.E_CONTINUE:
                try:
                    await existing_n_verified.delete()

                except disnake.Forbidden:
                    await db.PLUGINS.update_one(
                        await db.PLUGINS.find_one({"_id": ctx.guild.id}),
                        {"$set": {"Verification": False}},
                    )

                    await ctx.send(
                        embed=disnake.Embed(
                            title="Missing Permissions",
                            description=(
                                "🚫 I don't have permissions to delete the"
                                " existing role, due to this error verification"
                                " plugin has been disabled again"
                            ),
                            color=var.C_RED,
                        )
                    )
            if (
                str(reaction.emoji) == var.E_CONTINUE
                or str(reaction.emoji) == var.E_ACCEPT
            ):
                await setup()

        else:
            await setup()

    @commands.command(name="verifyinfo")
    @has_command_permission()
    async def verify_info(self, ctx):
        guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})

        verify_type = guild_doc.get("type")
        if verify_type == "command":
            embed = disnake.Embed(
                title=f"This server has Command verification",
                description=(
                    "This is a basic type of verification where users enter a "
                    "command in the verification channel and they are quickly "
                    "verified and given access to other channels, this can be "
                    "used to verify people and low-medium level raid/spam bot."
                ),
                color=var.C_TEAL,
            )

        else:
            embed = disnake.Embed(
                title="This server has Bot verification",
                description=(
                    "This is a slightly more advanced bot captcha like "
                    "verification most suitable to bypass advance bot raids, "
                    "after users enter the command a captcha image is sent in "
                    "the channel with distorted text (good enough for a human "
                    "to read) and if the users enter the code correctly they"
                    " are verified. The image lasts only for 15 seconds, "
                    "entering the command again will send another new image."
                ),
                color=var.C_TEAL,
            )

        embed.add_field(
            name="Verification Channel",
            value=self.bot.get_channel(guild_doc.get("channel")).mention,
        )

        embed.add_field(
            name="Not Verified Role",
            value=ctx.guild.get_role(guild_doc.get("roleid")).mention,
        )

        if guild_doc.get("assignrole") is None:
            role = None

        else:
            role = ctx.guild.get_role(guild_doc.get("assignrole")).mention

        embed.add_field(name="Verified Role", value=role)
        await ctx.send(embed=embed)

    @commands.command(name="verifychannel")
    @has_command_permission()
    async def verify_channel(self, ctx, channel: disnake.TextChannel = None):
        if channel is not None:
            guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})
            n_verified = ctx.guild.get_role(guild_doc.get("roleid"))

            await self.bot.get_channel(guild_doc.get("channel")).set_permissions(
                ctx.guild.default_role, view_channel=True
            )

            await self.bot.get_channel(guild_doc.get("channel")).set_permissions(
                n_verified, view_channel=False
            )

            new_data = {"$set": {"channel": channel.id}}

            await db.VERIFY.update_one(guild_doc, new_data)
            await self.bot.get_channel(channel.id).set_permissions(
                n_verified, view_channel=True
            )

            embed = disnake.Embed(
                title="Successfully changed the verification channel",
                description=(f"Members will now be verified in {channel.mention}!"),
                color=var.C_BLUE,
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the" " verification channel to change it"
                    ),
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}verifychannel <#channel>`",
                )
            )

    @commands.command(name="verifyswitch")
    @has_command_permission()
    async def verify_switch(self, ctx):
        guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})
        if guild_doc.get("type") == "command":
            new_data = {"$set": {"type": "bot"}}

        else:
            new_data = {"$set": {"type": "command"}}

        await db.VERIFY.update_one(guild_doc, new_data)

        await ctx.send(
            embed=disnake.Embed(
                title=(
                    "Switched to " + new_data.get("$set").get("type") + " verification"
                ),
                description=("Use the command again to switch to the other method"),
                color=var.C_GREEN,
            )
        )

    @commands.command(name="verifyrole")
    @has_command_permission()
    async def verify_role(self, ctx, role: disnake.Role = None):
        if role is not None:
            guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})
            new_data = {"$set": {"assignrole": role.id}}

            await db.VERIFY.update_one(guild_doc, new_data)

            await ctx.send(
                embed=disnake.Embed(
                    description=(f"{var.E_ACCEPT} Successfully added {role.mention}"),
                    color=var.C_GREEN,
                ).set_footer(
                    text=(
                        "Now users who will successfully" " verify will get this role"
                    )
                )
            )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description="🚫 You need to define the role too!", color=var.C_RED
                )
                .add_field(
                    name="Format", value=f"`{await get_prefix(ctx)}verifyrole <role>`"
                )
                .set_footer(
                    text=(
                        "For role either role mention"
                        " or ID can be used "
                        "(to not disturb anyone having the role)"
                    )
                )
            )

    @commands.command(name="verifyroleremove")
    @has_command_permission()
    async def verify_role_remove(self, ctx):
        guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})

        if guild_doc.get("assignrole") is not None:
            role = ctx.guild.get_role(guild_doc.get("assignrole"))

            new_data = {"$set": {"assignrole": None}}

            await db.VERIFY.update_one(guild_doc, new_data)

            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_ACCEPT} Removed {role.mention}" " from verified role"
                    ),
                    color=var.C_GREEN,
                ).set_footer(
                    text="Now users who verify successfully won't get this role"
                )
            )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description="🚫 You need to define the role too!", color=var.C_RED
                )
                .add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}verifyroleremove <role>`",
                )
                .set_footer(
                    text=(
                        "For role either role mention or ID can be used"
                        " (to not disturb anyone having the role)"
                    )
                )
            )

    @commands.command(name="verifyremove")
    @has_command_permission()
    async def verify_remove(self, ctx):
        guild_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})

        await db.VERIFY.delete_one(guild_doc)
        await disnake.utils.get(ctx.guild.roles, name="Not Verified").delete()

        guild_plugin_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        new_data = {"$set": {"Verification": False}}

        await db.PLUGINS.update_one(guild_plugin_doc, new_data)
        await ctx.send("Successfully removed verification from this server!")

    @commands.command(aliases=["verifyme"])
    async def verify(self, ctx):
        # Verify channel IDs
        if ctx.channel.id in await db.VERIFY.distinct("channel"):
            verify_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})

            if verify_doc["type"] == "command":  # Command based verification
                role_id = verify_doc["roleid"]
                role = ctx.guild.get_role(role_id)

                await ctx.send(
                    (
                        f"{var.E_ACCEPT} "
                        f" Verification successful **```{ctx.author}```**"
                    ),
                    delete_after=1,
                )

                await ctx.author.remove_roles(role)

                if verify_doc["assignrole"] is not None:
                    await ctx.author.add_roles(
                        ctx.guild.get_role(verify_doc["assignrole"])
                    )

            else:
                # Bot verification
                # Lookin epic innit bruv?

                base = "https://cdn.discordapp.com/attachments/807140294764003350"

                images = {
                    f"{base}/808170831586787398/": "7h3fpaw1",
                    f"{base}/808170832744415283/": "bs4hm1gd",
                    f"{base}/808170834514018304/": "kp6d1vs9",
                    f"{base}/808170834484789309/": "hmxe425",
                    f"{base}/808170835957383189/": "jd3573vq",
                }

                choice = random.choice(list(images))
                code = images[choice]
                url = choice + code + ".png"
                print(url)
                embed = (
                    disnake.Embed(
                        title="Beep Bop,  are you a bot?",
                        description=(
                            "Enter the text given in the image"
                            " below to verify yourself"
                        ),
                        colour=var.C_MAIN,
                    )
                    .set_image(url=url)
                    .set_footer(
                        text=(
                            "You have 20 seconds to enter the text, "
                            "if you failed to enter it in time then "
                            "type the command again."
                        )
                    )
                )

                bot_msg = await ctx.send(embed=embed, delete_after=20.0)

                def code_check(message):
                    return (
                        message.author == ctx.author
                        and message.channel.id == ctx.channel.id
                    )

                try:
                    user_msg = await self.bot.wait_for(
                        "message", check=code_check, timeout=20.0
                    )

                    if user_msg.content == code:
                        role_id = verify_doc["roleid"]
                        role = ctx.guild.get_role(role_id)

                        await ctx.send(
                            (
                                f"{var.E_ACCEPT}  Verification "
                                f"successful **```{ctx.author}```**"
                            ),
                            delete_after=1,
                        )

                        await ctx.author.remove_roles(role)

                        if verify_doc["assignrole"] is not None:
                            await ctx.author.add_roles(
                                ctx.guild.get_role(verify_doc["assignrole"])
                            )

                        await bot_msg.delete()

                    else:
                        await ctx.send("Wrong, try again", delete_after=1)
                        await bot_msg.delete()

                except asyncio.TimeoutError:
                    pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        plugin_doc = await db.PLUGINS.find_one({"_id": message.guild.id})

        if plugin_doc["Verification"]:
            guild_verify_doc = await db.VERIFY.find_one({"_id": message.guild.id})

            if guild_verify_doc is None:
                print(f"First time verification being enabled", message.guild.name)

            elif (
                message.channel.id == guild_verify_doc["channel"]
                and message.author != self.bot.user
            ):
                await message.delete()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        verify_doc = await db.VERIFY.find_one({"_id": member.guild.id})
        plugin_doc = await db.PLUGINS.find_one({"_id": member.guild.id})

        if plugin_doc["Verification"]:
            role_id = verify_doc["roleid"]
            unverified_role = member.guild.get_role(role_id)

            await member.add_roles(unverified_role)


def setup(bot):
    bot.add_cog(Verification(bot))
