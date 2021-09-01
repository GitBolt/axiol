from __future__ import annotations
from typing import TYPE_CHECKING

from discord import ActivityType, Activity
from discord.ext import tasks

if TYPE_CHECKING:
    from axiol.core.bot import Bot


@tasks.loop(minutes=1)
async def update_presence(bot: Bot):
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"{bot.default_prefix}help | {bot.latency * 1000:,.3f}ms"
        )
    )
