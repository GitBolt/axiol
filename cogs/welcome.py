from discord.ext import commands
import utils.vars as var

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guildverify = var.VERIFY.find_one({"_id": member.guild.id})
        if guildverify is not None:
            roleid = guildverify.get("roleid")
            role = member.guild.get_role(roleid)
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(Welcome(bot))