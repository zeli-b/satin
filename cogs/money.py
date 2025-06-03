from random import randint
from re import compile

from discord import Interaction, Message
from discord.app_commands import command, describe
from discord.ext.commands import Cog, Bot

from currency import get_money, UNIT, rotate, set_money


class MoneyCog(Cog):
    @Cog.listener()
    async def on_message(self, message: Message):
        # give money by message
        amount = rotate(len(set(message.content)))
        having = get_money(message.author.id)
        set_money(message.author.id, having + amount)

    @command(name="money", description="소지금을 확인합니다")
    async def money(self, ctx: Interaction):
        amount = get_money(ctx.user.id)

        await ctx.response.send_message(f"{amount:,} {UNIT}")


async def setup(bot: Bot):
    await bot.add_cog(MoneyCog(bot))
