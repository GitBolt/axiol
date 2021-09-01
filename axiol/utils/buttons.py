import discord
from axiol.utils.constants import Emojis
class Paginator(discord.ui.View):
    def __init__(
            self, 
            bot,
            context,
            page_type, 
            total_pages, 
            embed, 
            data_list, 
        ):
        self.bot = bot
        self.context = context
        self.page_type = page_type
        self.total_pages = total_pages
        self.embed = embed
        self.data_list = data_list

        self.page = 1
        super().__init__(timeout=60)

    async def on_timeout(self):
        self.embed.set_footer(text=f"{self.embed.footer.text}\nButtons have been cleared due 60 seconds of inactivity")
        await self.message.edit(embed=self.embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user == self.context.author:
            await interaction.response.send_message("You can't press buttons in someone else's command.", ephemeral=True)
        return interaction.user == self.context.author  

    async def change_page(self):
        self.embed.set_footer(text=f"Page {self.page}/{self.total_pages}")
        self.embed.clear_fields()
        item_count = self.page*10 if self.page != 1 else 0

        for i in self.data_list[int((self.page*10)-10):int(self.page*10)]:
            item_count += 1
            if self.page_type == "rr":
                message_id = i["messageid"]
                role = self.context.guild.get_role(i["roleid"])
                emoji = i["emoji"]
                self.embed.add_field(name=f"{emoji} in {message_id}", value=f"for {role.mention}", inline=False)
            else:
                user = self.bot.get_user(i["_id"])
                xp = i.get("xp")
                self.embed.add_field(name=f"{item_count}. {user}", value=f"Total XP: {xp}", inline=False)

    
    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.blurple, disabled=True)
    async def first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.page = 1
        await self.change_page()
        self.children[0].disabled, self.children[1].disabled = True, True
        self.children[2].disabled, self.children[3].disabled = False, False
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.grey, disabled=True)
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.page -= 1
        await self.change_page()
        self.children[2].disabled, self.children[3].disabled = False, False
        self.children[0].disabled = False if self.page != 1 else True
        self.children[1].disabled = False if self.page != 1 else True
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.grey)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.page += 1
        await self.change_page()
        self.children[0].disabled, self.children[1].disabled = False, False
        self.children[2].disabled = False if self.page != self.total_pages else True
        self.children[3].disabled = False if self.page != self.total_pages else True
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)
    async def last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.page = self.total_pages
        await self.change_page()
        self.children[0].disabled, self.children[1].disabled = False, False
        self.children[2].disabled, self.children[3].disabled = True, True
        await interaction.response.edit_message(embed=self.embed, view=self)


class Enable(discord.ui.View):
    def __init__(self, context):
        self.context = context
        self.value = None
        self.type = True
        super().__init__(timeout=60)

    async def on_timeout(self):
        self.embed.set_footer(text=f"{self.embed.footer.text}\nButtons have been cleared due 60 seconds of inactivity")
        await self.message.edit(embed=self.embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user == self.context.author:
            await interaction.response.send_message("You can't press buttons in someone else's command.", ephemeral=True)
        return interaction.user == self.context.author  

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await self.message.edit(view=None)
        await interaction.response.send_message("Cancelled plugin switch.")
        self.stop()

    @discord.ui.button(label="Enable", emoji=Emojis.ENABLE.value, style=discord.ButtonStyle.green)
    async def enable(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        await self.message.edit(view=None)
        self.stop()


class Disable(discord.ui.View):
    def __init__(self, context, embed):
        self.context = context
        self.value = None
        self.type = False
        self.embed = embed
        super().__init__(timeout=60)

    async def on_timeout(self):
        self.embed.set_footer(text=f"{self.embed.footer.text}\nButtons have been cleared due 60 seconds of inactivity")
        await self.message.edit(embed=self.embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user == self.context.author:
            await interaction.response.send_message("You can't press buttons in someone else's command.", ephemeral=True)
        return interaction.user == self.context.author  

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await self.message.edit(view=None)
        await interaction.response.send_message("Cancelled plugin switch.")
        self.stop()

    @discord.ui.button(label="Disable", emoji=Emojis.DISABLE.value, style=discord.ButtonStyle.red)
    async def disable(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        await self.message.edit(view=None)
        self.stop()


class Plugins(discord.ui.View):
    def __init__(
            self, 
            bot,
            context,
            embed, 
        ):
        self.bot = bot
        self.context = context
        self.embed = embed

        self.plugin = None
        super().__init__(timeout=60)

    async def on_timeout(self):
        await self.message.edit(view=None)

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user == self.context.author:
            await interaction.response.send_message("You can't press buttons in someone else's command.", ephemeral=True)
        return interaction.user == self.context.author  


    @discord.ui.button(emoji="🛡️", style=discord.ButtonStyle.grey)
    async def automod(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "AutoMod"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="🤖", style=discord.ButtonStyle.grey)
    async def chatbot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Chatbot"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="🎯", style=discord.ButtonStyle.grey)
    async def fun(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Fun"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="🎉", style=discord.ButtonStyle.grey)
    async def fun(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Giveaway"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="🎭", style=discord.ButtonStyle.grey)
    async def karma(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Karma"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji=Emojis.LEVELING.value, style=discord.ButtonStyle.grey)
    async def leveling(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Leveling"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="🔨", style=discord.ButtonStyle.grey)
    async def moderation(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Moderation"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="✨", style=discord.ButtonStyle.grey)
    async def reactionroles(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "ReactionRoles"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="✅", style=discord.ButtonStyle.grey)
    async def verification(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin ="Verification"
        await self.message.edit(view=None)
        self.stop()

    @discord.ui.button(emoji="👋", style=discord.ButtonStyle.grey)
    async def welcome(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.plugin = "Welcome"
        await self.message.edit(view=None)
        self.stop()