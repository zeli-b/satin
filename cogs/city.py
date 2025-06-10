from math import log10
from discord import Interaction
from discord.app_commands import command, describe, Group, checks
from discord.ext.commands import Cog, Bot
from discord.ext.tasks import loop

from consts import get_const
from libs import city, currency


def payment(name):
    pop = city.get_population(name)
    are = city.get_area(name)
    dom = city.get_dominance(name)
    man = city.get_management(name)

    ecy_delta = 0
    pop_delta = 0
    dom_delta = 0

    pop_delta += round(pop * 2.1 ** (1/440))
    ecy_delta -= round(pop * arr / 100000)
    dom_delta -= (log10(pop) - 3) / 100
    ecy_delta -= round(pop * (1 - dom) / 10 * man)
    dom_delta += man / 100
    ecy_delta -= round(pop / 100 * k)
    ecy_delta += round((pop**1.1 - 1000) / 20)
    dom_delta -= abs((3.5 - log10(pop / are)) / 100)

    city.set_population(pop + pop_delta)
    city.set_area(are + are_delta)
    city.set_dominance(dom + dom_delta)


class CityCog(Cog):
    @loop(seconds=get_const("city.payment-loop-sec"))
    async def loop_payment(self):
        for name in city.get_city_names():
            payment(name)
            print(f"payment for {name}")
        print(f"payment done")
    
    city_group = Group(name="도시", description="도시를 관리합니다")

    @city_group.command(name="건설", description="도시 건설하기")
    @describe(name="도시 이름", owner="법인")
    @checks.has_role("관리자")
    async def city_create(self, ctx: Interaction, name: str, owner: str):
        if city.is_city(name):
            await ctx.response.send_message("이름 중복", ephemeral=True)
            return
        
        if not currency.is_account(owner):
            await ctx.response.send_message("없는 법인", ephemeral=True)
            return

        city.create_city(name, owner)
        await ctx.response.send_message("도시 건설함. 7,000 mE 징수할 것")

    @city_group.command(name="면적", description="도시 면적 설정하기")
    @describe(name="도시 이름", area="도시 면적 (km^2)")
    @checks.has_role("관리자")
    async def city_area(self, ctx: Interaction, name: str, area: float):
        if not city.is_city(name):
            await ctx.response.send_message("없는 도시", ephemeral=True)
            return

        city.set_area(name, area)
        await ctx.response.send_message("면적 설정함")

    @city_group.command(name="인구", description="도시 인구 설정하기")
    @describe(name="도시 이름", population="도시 인구 (명)")
    @checks.has_role("관리자")
    async def city_population(self, ctx: Interaction, name: str, population: int):
        if not city.is_city(name):
            await ctx.response.send_message("없는 도시", ephemeral=True)
            return

        city.set_population(name, population)
        await ctx.response.send_message("인구 설정함")

    @city_group.command(name="정보", description="도시의 정보를 확인합니다")
    @describe(name="도시 이름")
    async def city_settle(self, ctx: Interaction, name: str):
        if not city.is_city(name):
            await ctx.response.send_message("없는 도시", ephemeral=True)
            return

        owner = city.get_owner_account(name)
        area = city.get_area(name)
        population = city.get_population(name)
        content = f"{name}. {owner} 소유. {area:,} km2, {population:,}명"
        await ctx.response.send_message(content)

    @city_group.command(name="영수증", description="마지막 정산의 영수증을 확인")
    @describe(name="도시 이름")
    async def city_settle(self, ctx: Interaction, name: str):
        await ctx.response.send_message("구현안됨")


async def setup(bot: Bot):
    await bot.add_cog(CityCog(bot))
