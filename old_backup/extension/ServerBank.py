import discord
from discord.ext import commands
from db.players_db import players
from db.bank_db import get_discord_id


class ServerBankCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bank")
    async def bank_command(self, ctx):
        member = ctx.author
        player = players(member.id)
        coins = "${:,d}".format(player[5])
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
                f"Bank ID : {player[4]}\n"
                f"Total coins : {coins}\n",
                mention_author=False
            )
            return
        else:
            await ctx.reply('Only type commands in <#937364944498856026> channel', mention_author=False)

    @commands.command(name="status")
    async def status_command(self, ctx):
        member = ctx.author
        player = players(member.id)
        coins = "${:,d}".format(player[5])
        if player is None:
            await ctx.reply("⚠ Your information not found.", mention_author=False)
            return
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            await ctx.reply(
                "================================\n"
                "🛡 **YOUR STATUS INFORMATION**\n"
                f"Discord Name : {player[1]}\n"
                f"Steam ID : {player[3]}\n"
                f"Bank ID : {player[4]}\n"
                f"Total coins : {coins}\n"
                f"Level : {player[6]}\n"
                f"Exp : {player[7]}\n",
                mention_author=False,
            )
            return
        else:
            await ctx.reply(
                "Only used command in <#937364944498856026> channel",
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
                "Your Coins is : ${:,d}".format(player[5]), mention_author=False
            )
            return
        else:
            await ctx.reply(
                "Only used command in <#937364944498856026> channel",
                mention_author=False,
            )
            return

    @commands.command(name='transfer')
    async def transfer_command(self, ctx, amount, guild_id):
        member = ctx.author
        player = players(member.id)
        transfer_coin = int(amount)
        receipt_id = get_discord_id(guild_id)
        receipt = players(receipt_id)
        receipt_coin = int(receipt[5])
        if (
                ctx.channel.id == 937364944498856026
                or ctx.author.guild_permissions.administrator
        ):
            if transfer_coin <= int(player[5]):
                minus = int(player[5]) - int(transfer_coin)
                plus = int(receipt_coin) + int(amount)
                await ctx.reply(
                    'You transfer ${:,d} to **{}** successfull. \nYour current balance is ${:,d}'.format(int(amount),
                                                                                                         receipt[1],
                                                                                                         int(minus)),
                    mention_author=False)
                print(minus)
                return
            else:
                await ctx.reply(f'{member.name} : ⚠ Your coin not '
                                'enough for use this command.',
                                mention_author=False)
                return
        else:
            await ctx.reply(
                "Only used command in <#937364944498856026> channel",
                mention_author=False,
            )
            return

    @transfer_command.error
    async def transfer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Require argument. ```diff\n!transfer [amount] [bank_id]\n```', mention_author=False)


def setup(bot):
    bot.add_cog(ServerBankCommand(bot))
