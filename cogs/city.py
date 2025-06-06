from discord import Interaction
from discord.app_commands import command, describe, Group
from discord.ext.commands import Cog, Bot


class CityCog(Cog):
    city_group = Group(name="도시", description="도시를 관리합니다")

    @city_group.command(name="건설", description="도시 건설하기")
    @describe(name="도시 이름", owner="법인")
    async def city_create(self, ctx: Interaction, name: str, owner: str):
        await ctx.response.send_message("구현안됨")

    @city_group.command(name="면적", description="도시 면적 설정하기")
    @describe(name="도시 이름", area="도시 면적 (km^2)")
    async def city_area(self, ctx: Interaction, name: str, area: float):
        await ctx.response.send_message("구현안됨")

    @city_group.command(name="인구", description="도시 인구 설정하기")
    @describe(name="도시 이름", population="도시 인구 (명)")
    async def city_population(self, ctx: Interaction, name: str, population: int):
        await ctx.response.send_message("구현안됨")

    @city_group.command(name="영수증", description="마지막 정산의 영수증을 확인")
    @describe(name="도시 이름")
    async def city_settle(self, ctx: Interaction, name: str):
        await ctx.response.send_message("구현안됨")


async def setup(bot: Bot):
    await bot.add_cog(CityCog(bot))
