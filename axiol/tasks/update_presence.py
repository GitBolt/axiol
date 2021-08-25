from __future__ import annotations
from typing import TYPE_CHECKING

from discord import ActivityType, Activity
from discord.ext import tasks

if TYPE_CHECKING:
    from core.bot import Bot


@tasks.loop(minutes=1)
async def update_presence(client: Bot):
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"{client.command_prefix}help | {client.latency * 1000:,.3f}ms"
        )
    )
