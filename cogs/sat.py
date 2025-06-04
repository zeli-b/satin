from datetime import datetime

from discord import Interaction
from discord.app_commands import command, describe, Group
from discord.ext.commands import Cog, Bot

from util import abeliqua


class SatCog(Cog):
    abeliqua_group = Group(name="아벨리카력", description="아벨리카력 변환")

    @abeliqua_group.command(name="으로", description="아벨리카력으로 변환")
    @describe(time="시각 (YYYY-MM-DD hh:mm:ss)")
    async def abeliqua_to(self, ctx: Interaction, time: str = ""):
        try:
            time = datetime.fromisoformat(time)
        except ValueError:
            time = datetime.now()

        abtime = abeliqua.format(abeliqua.from_datetime(time))
        await ctx.response.send_message(abtime)


async def setup(bot: Bot):
    await bot.add_cog(SatCog(bot))
