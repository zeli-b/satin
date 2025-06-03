from random import randint
from re import compile

from discord import Interaction
from discord.app_commands import command, describe
from discord.ext.commands import Cog, Bot


class UtilCog(Cog):
    @command(name="dice", description="주사의를 굴립니다")
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


async def setup(bot: Bot):
    await bot.add_cog(UtilCog(bot))
