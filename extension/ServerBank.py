from discord.ext import commands

from database.Bank_db import coins, get_coins, update_coins
from database.players import players


class ServerBankCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bank")
    async def bank_command(self, ctx):
        member = ctx.author
        player = players(member.id)
        if player is None:
            await ctx.reply("⚠ Your information not found.", mention_author=False)
            return
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            await ctx.reply(
                "================================\n"
                "**🏦 YOUR BANK INFORMATION**\n"
                f"Discord Name : {player[1]}\n"
                f"Bank ID : {player[9]}\n"
                f"Total coins : {player[10]}\n"
                "================================",
                mention_author=False,
            )
            return

    @commands.command(name="status")
    async def status_command(self, ctx):
        member = ctx.author
        player = players(member.id)
        if player is None:
            await ctx.reply("⚠ Your information not found.", mention_author=False)
            return
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            await ctx.reply(
                "================================\n"
                "📖 **YOUR STATUS INFORMATION**\n"
                f"Discord Name : {player[1]}\n"
                f"Steam ID : {player[3]}\n"
                f"Bank ID : {player[9]}\n"
                f"Total coins : {player[10]}\n"
                f"Level : {player[4]}\n"
                f"Exp : {player[5]}\n"
                "================================",
                mention_author=False,
            )
            return

    @commands.command(name="my_coins")
    async def my_coins_command(self, ctx):
        member = ctx.author
        player = players(member.id)
        if player is None:
            await ctx.reply("⚠ Your information is not found", mention_author=False)
            return
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            await ctx.reply(
                "Your Coins is : {}".format(player[10]), mention_author=False
            )

    @commands.command(name='transfer')
    async def transfer_command(self, ctx, amount, bank_id):
        member = ctx.author
        owner = get_coins(member.id)

        receipt = coins(bank_id)
        receipt_id = receipt[1]
        receipt_coin = receipt[0]
        transfer_coin = int(amount)
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            if transfer_coin <= int(owner):
                minus = int(owner) - transfer_coin
                plus = int(receipt_coin) + int(amount)
                update_coins(minus, member.id)
                update_coins(plus, receipt_id)
                await ctx.reply(
                    f'{member.name} transfer {amount} to {bank_id} '
                    f'successfully (your balance is {minus} : {plus}).',
                    mention_author=False)
                return
            else:
                await ctx.reply(f'{member.name} : ⚠ Your coin not '
                                'enough for use this command.',
                                mention_author=False)
                return
        else:
            await ctx.reply(
                "Only used command in <#937364944498856026>",
                mention_author=False,
            )
            return

    @transfer_command.error
    async def transfer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Require argument. ```diff\n!transfer [amount] [bank_id]\n```', mention_author=False)


def setup(bot):
    bot.add_cog(ServerBankCommand(bot))
