from random import randint
from re import compile

from discord import Interaction, Message, User
from discord.app_commands import command, describe, Group
from discord.ext.commands import Cog, Bot

from libs.currency import get_money, UNIT, rotate, set_money, get_owners, \
        set_owners, get_accounts_of, is_account, freeze, get_tax, set_tax
from libs.attendance import attend, get_record


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

    account_group = Group(name="법인", description="법인 관련 명령어")

    @account_group.command(
        name="개설",
        description=f"법인을 개설합니다. 100 {UNIT}이 필요합니다."
    )
    async def account_create(self, ctx: Interaction, name: str):
        if is_account(name):
            await ctx.response.send_message("이미 이름 존재", ephemeral=True)
            return

        having = get_money(ctx.user.id)
        if having < 100:
            await ctx.response.send_message("잔액부족", ephemeral=True)
            return

        amount = freeze(100)
        set_money(ctx.user.id, having - amount)

        set_owners(name, [ctx.user.id])

        await ctx.response.send_message("법인 개설됨")

    @account_group.command(name="목록", description="가지고 있는 법인 목록 보기")
    async def account_list(self, ctx: Interaction):
        accounts = get_accounts_of(ctx.user.id)
        
        if not accounts:
            await ctx.response.send_message("법인 없음")
            return

        content = ", ".join(accounts)
        await ctx.response.send_message(content)

    @account_group.command(name="충전", description=f"법인 잔액을 충전합니다")
    async def account_charge(self, ctx: Interaction, name: str, amount: int):
        if not is_account(name):
            await ctx.response.send_message("법인 없음", ephemeral=True)
            return

        having = get_money(ctx.user.id)
        if having < amount:
            await ctx.response.send_message("잔액부족", ephemeral=True)
            return

        acc_having = get_money(name)
        set_money(ctx.user.id, having - amount)
        set_money(name, acc_having + amount)

        await ctx.response.send_message("송금함")

    @account_group.command(name="확인", description=f"법인 잔액을 확인합니다")
    async def account_check(self, ctx: Interaction, name: str):
        accounts = get_accounts_of(ctx.user.id)
        if name not in accounts:
            await ctx.response.send_message("소유권 없음")
            return

        having = get_money(name)
        await ctx.response.send_message(f"{having:,} {UNIT}")

    @account_group.command(name="삭제", description=f"법인을 삭제합니다")
    async def account_remove(self, ctx: Interaction, name: str):
        return await ctx.response.send_message("구현안됨")

    @account_group.command(name="송금", description=f"법인에서 송금합니다")
    async def account_send(self, ctx: Interaction, name: str, to: User, amount: int):
        return await ctx.response.send_message("구현안됨")

    @account_group.command(name="세금", description=f"법인의 미납 세금을 확인합니다")
    async def account_tax(self, ctx: Interaction, name: str):
        if not is_account(name):
            await ctx.response.send_message("법인 불명", ephemeral=True)
            return

        tax = get_tax(name)
        await ctx.response.send_message(f"{tax:,} {UNIT}")

    @account_group.command(name="납세", description="법인이 세금을 납세합니다")
    async def account_pay(self, ctx: Interaction, name: str, amount: int = 0):
        if amount < 0:
            await ctx.response.send_message("금액 이상함", ephemeral=True)
            return

        if not is_account(name):
            await ctx.response.send_message("법인 불명", ephemeral=True)
            return

        tax = get_tax(name)
        having = get_money(name)

        if amount == 0:
            amount = min(having, tax)

        if amount > having:
            await ctx.response.send_message("잔액부족", ephemeral=True)
            return

        set_tax(name, tax - amount)
        set_money(name, having - amount)

        await ctx.response.send_message("납세함")

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
