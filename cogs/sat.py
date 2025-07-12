from re import compile
from datetime import datetime

from discord import Interaction
from discord.app_commands import describe, Group
from discord.ext.commands import Cog, Bot

from libs import abeliqua


class SatCog(Cog):
    abeliqua_group = Group(name="아벨리카력", description="아벨리카력 변환")

    @abeliqua_group.command(name="으로", description="아벨리카력으로 변환")
    @describe(time="시각 (YYYY-MM-DD hh:mm:ss)")
    async def abeliqua_to(self, ctx: Interaction, time: str = ""):
        try:
            dtime = datetime.fromisoformat(time)
        except ValueError:
            dtime = datetime.now()

        abtime = abeliqua.format(abeliqua.from_datetime(dtime))
        await ctx.response.send_message(abtime)

    @abeliqua_group.command(name="에서", description="아벨리카력에서 변환")
    @describe(time="시각 (YY-MM-DD (hh:mm(:ss)))")
    async def abeliqua_from(self, ctx: Interaction, time: str = ""):
        ABTIME_RE = compile(r'(\d+)-(\d+)-(\d+)( (\d+):(\d+)(:(\d+))?)?')

        if not ABTIME_RE.match(time):
            await ctx.response.send_message("시각 형식이 이상합니다.", ephemeral=True)
            return

        year, month, day, _, hour, minute, _, second = ABTIME_RE.findall(time)[0]
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour) if hour else 0
        minute = int(minute) if minute else 0
        second = int(second) if second else 0

        result = abeliqua.to_datetime((year, month, day, hour, minute, second))

        await ctx.response.send_message(f'{result}')


async def setup(bot: Bot):
    await bot.add_cog(SatCog(bot))
