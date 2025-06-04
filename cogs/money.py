from random import randint
from re import compile

from discord import Interaction, Message, User
from discord.app_commands import command, describe, Group
from discord.ext.commands import Cog, Bot

from libs.currency import get_money, UNIT, rotate, set_money
from libs.attendance import attend, get_ranking


class MoneyCog(Cog):
    @Cog.listener()
    async def on_message(self, message: Message):
        # give money by message
        amount = rotate(len(set(message.content)))
        having = get_money(message.author.id)
        set_money(message.author.id, having + amount)

    money_group = Group(name="돈", description="돈 관련 기능")

    @money_group.command(name="확인", description="소지금을 확인합니다")
    async def money_check(self, ctx: Interaction):
        amount = get_money(ctx.user.id)

        await ctx.response.send_message(f"{amount:,} {UNIT}")
    
    @money_group.command(name="송금", description="돈을 송금합니다.")
    async def money_send(self, ctx: Interaction, to: User, amount: int):
        if amount <= 0:
            await ctx.response.send_message("송금액이 이상합니다.", ephemeral=True)
            return

        having = get_money(ctx.user.id)
        if having < amount:
            await ctx.response.send_message("돈이 부족합니다.", ephemeral=True)
            return

        set_money(ctx.user.id, having - amount)

        them_having = get_money(to.id)
        set_money(to.id, them_having + amount)

        await ctx.response.send_message("돈을 송금했습니다.")

    attend_group = Group(name="출석", description="출석 관련 명령어")

    @attend_group.command(name="체크", description="출석합니다")
    async def attend(self, ctx: Interaction):
        streak = attend(ctx.user.id)
        if streak == 0:
            await ctx.response.send_message("이미 오늘 출석")
            return

        having = get_money(ctx.user.id)
        bonus = rotate(streak * 100)

        set_money(ctx.user.id, having + bonus)
        record = get_record(ctx.user.id)
        content = f"{streak}일 연속 출석. " \
                  f"{bonus:,} {UNIT} 지급. 최고기록 {record}일"

        await ctx.response.send_message(content)


async def setup(bot: Bot):
    await bot.add_cog(MoneyCog(bot))
