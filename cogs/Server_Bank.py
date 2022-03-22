import discord
from discord.ext import commands
from players.players_db import *


class ServerBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='transfer')
    async def transfer_command(self, ctx, bank_id: int, amount: int):
        guild = self.bot.get_guild(908064048728387604)
        member = ctx.author
        member_bank_id = players_discord(ctx.author.id)
        payer_coins = players_bank(member_bank_id)
        receipt_player = players_bank(bank_id)
        receipts = get_discord_id(bank_id)
        receipt_players = players(receipts)
        message = None
        if payer_coins < amount:
            message = "ยอดเงินของคุณมีไม่พอสำหรับการโอนเงินในครั้งนี้"
        elif amount <= payer_coins:
            minut = payer_coins - amount
            plus = receipt_player + amount
            payers = update_player_coins(ctx.author.id, minut)
            receipt = update_player_coins(receipts, plus)
            total = get_player_coins(ctx.author.id)
            receipt_total  = get_player_coins(receipts)
            receipt_pl = guild.get_member(receipts)
            message = f"โอนเงิน จำนวน {amount} ให้กับ {receipt_players[1]} เรียบร้อยแล้ว"
            await ctx.reply(f"{message}", mention_author=False)
            receipt_message = f"คุณได้รับการโอนเงิน จาก {member.name}" \
                              f" จำนวน {amount} ยอดเงินทั้งหมดของคุณคือ {receipt_total}"
            await discord.DMChannel.send(receipt_pl, receipt_message)
            await discord.DMChannel.send(member, f"ยอดเงินคงเหลือของคุณเท่ากับ {total}")

    @transfer_command.error
    async def transfer_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)


def setup(bot):
    bot.add_cog(ServerBank(bot))
