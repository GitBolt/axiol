import sys
import traceback
import discord
from discord.ext import commands
from utils.variables import E_ERROR, C_RED


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        

        #Invalid Channel
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send(embed=discord.Embed(
                    title="Invalid Channel",
                    description=f"{E_ERROR} I was not able to find the channel which you entered",
                    color=C_RED
            ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
            )

        #Missing Permissions
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                        title="Missing Permissions",
                        description=f"{E_ERROR} {ctx.author.mention} You don't have permissions to do that",
                        color=C_RED
            ))

        #Cog check failure
        if isinstance(error, commands.CheckFailure):
            pass

        else:
            #All unhandled Errors will print their original traceback
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        

def setup(bot):
    bot.add_cog(Errors(bot))