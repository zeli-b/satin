from random import randint
from re import compile

from discord import Interaction
from discord.app_commands import command, describe, Group
from discord.ext.commands import Cog, Bot

from libs.memo import get_memo, set_memo


class UtilCog(Cog):
    @command(description="주사위를 굴립니다")
    @describe(dice="주사위 종류 (ndn+n)")
    async def search(self, ctx: Interaction, dice: str):
        re = compile(r"(\d+)?[dD](\d+)([+\-]\d+)?")
        die = re.findall(dice)

        if not die:
            await ctx.response.send_message("invalid die", ephemeral=True)
            return

        count, side, delta = die[0]
        count = int(count) if count else 1
        side = int(side)
        delta = int(delta) if delta else 0

        rolls = [randint(1, side) for _ in range(count)]
        eyes = sum(rolls) + delta
        message = " + ".join(map(str, rolls)) + f" + ({delta}) = __**{eyes}**__"

        await ctx.response.send_message(message)

    memo_group = Group(name="memo", description="메모를 작성하고 불러옵니다.")

    @memo_group.command(name="load", description="메모 보기")
    @describe(name="메모 이름")
    async def memo_load(self, ctx: Interaction, name: str):
        content = get_memo(name)
        if not content:
            await ctx.response.send_message("메모가 비어있습니다.")
            return

        await ctx.response.send_message(f">>> {content}")

    @memo_group.command(name="save", description="메모 쓰기")
    @describe(name="메모 이름", content="메모 내용")
    async def memo_save(self, ctx: Interaction, name: str, content: str = ""):
        set_memo(name, content)
        await ctx.response.send_message(f"메모 저장")


async def setup(bot: Bot):
    await bot.add_cog(UtilCog(bot))
