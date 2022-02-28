import asyncio

from discord.ext import commands

from bank.bank_db import update_coins
from players.players_db import players_exists, players, reset_daily_pack


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f'Logged in as {self.bot.user.name}')
    #     await self.bot.change_presence(
    #         status=discord.Status.online,
    #         activity=discord.Activity(type=discord.ActivityType.playing, name='SCUM')
    #     )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('clear'):
            if message.author.guild_permissions.administrator:
                await message.channel.purge()
                await message.channel.send('All message has been deleted.', mention_author=False, delete_after=2)
                return
            else:
                await message.channel.send('⚠ Error, You can not used this commands.', mention_author=False,
                                           delete_after=1)
                await asyncio.sleep(1)
                await message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply('⚠ Error, Commands not found in system.', mention_author=False)

    @commands.command(name='myinfo')
    async def myinfo_command(self, ctx):
        check = players_exists(ctx.author.id)  # return 0 or 1.
        if check == 0:
            await ctx.reply('Create new register player.', mention_author=False)
            return
        else:
            await ctx.reply("You're has been registered.", mention_author=False)

    @commands.command(name='addcoins')
    @commands.has_permissions(manage_roles=True)
    async def add_coions(self, ctx, amount: int, discord_id: int):
        check = players_exists(discord_id)
        if check == 1:
            player = players(discord_id)
            before_coins = player[5]
            marge = before_coins + amount
            update_coins(marge, discord_id)
            await ctx.reply('Add **${:,d}** to **{}** by system successfull.'.format(amount, player[1]),
                            mention_author=False)
        else:
            await ctx.reply(f'This **{discord_id}** could not be found in the database.', mention_author=False)

    @add_coions.error
    async def add_coin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('*This command can only be used by administrators.*', mention_author=False)

    @commands.command(name='removecoins')
    @commands.has_permissions(manage_roles=True)
    async def remove_coions(self, ctx, amount: int, discord_id: int):
        check = players_exists(discord_id)
        if check == 1:
            player = players(discord_id)
            before_coins = player[5]
            marge = before_coins - amount
            update_coins(marge, discord_id)
            await ctx.reply('Remove **${:,d}** to **{}** by system successfull.'.format(amount, player[1]),
                            mention_author=False)
        else:
            await ctx.reply(f'This **{discord_id}** could not be found in the database.', mention_author=False)

    @remove_coions.error
    async def remove_coin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('*This command can only be used by administrators.*', mention_author=False)

    @commands.command(name='load')
    @commands.has_permissions(manage_roles=True)
    async def load_command(self, ctx, ext):
        self.bot.load_extension(f'extension.{ext}')
        await ctx.reply(f'{ext} is loaded.', mention_author=False)

    @load_command.error
    async def load_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = 'You are missing the required premission to run this command!'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing a required argument: {error.param}'
        elif isinstance(error, commands.ExtensionNotFound):
            message = str(error)
        else:
            message = "Something went wrong whlie running the commands"

        await ctx.reply(message, mention_author=False)

    @commands.command(name='unload')
    @commands.has_permissions(manage_roles=True)
    async def unload_command(self, ctx, ext):
        self.bot.unload_extension(f'extension.{ext}')
        await ctx.reply(f'{ext} is unloaded.', mention_author=False)

    @unload_command.error
    async def unload_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = 'You are missing the required premission to run this command!'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing a required argument: {error.param}'
        elif isinstance(error, commands.ExtensionNotFound):
            message = str(error)
        else:
            message = "Something went wrong whlie running the commands"

        await ctx.reply(message, mention_author=False)

    @commands.command(name='reload')
    @commands.has_permissions(manage_roles=True)
    async def reload_command(self, ctx, ext):
        self.bot.unload_extension(f'extension.{ext}')
        self.bot.load_extension(f'extension.{ext}')
        await ctx.reply(f'{ext} is reloaded.', mention_author=False)

    @reload_command.error
    async def reload_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = 'You are missing the required premission to run this command!'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing a required argument: {error.param}'
        elif isinstance(error, commands.ExtensionNotFound):
            message = str(error)
        else:
            message = "Something went wrong whlie running the commands"

        await ctx.reply(message, mention_author=False)

    @commands.command(name='check')
    @commands.has_permissions(manage_roles=True)
    async def check_command(self, ctx, arg):
        check = players_exists(arg)
        if check == 1:
            player = players(arg)
            message = '```css\n===============================================\n' \
                      f'Discord Name: {player[1]}\n' \
                      f'Discord ID: {player[2]}\n' \
                      f'Steam ID: {player[3]}\n' \
                      f'Status : {player[9]}\n' \
                      f'===============================================\n' \
                      f'```'
            await ctx.reply(message, mention_author=False)
        else:
            await ctx.reply(f'This **{arg}** could not be found in the database.', mention_author=False)

    @check_command.error
    async def check_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = 'You are missing the required premission to run this command!'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing a required argument: {error.param}'
        else:
            message = "Something went wrong whlie running the commands"

        await ctx.reply(message, mention_author=False)

    @commands.command(name="reset_daily")
    @commands.has_permissions(manage_roles=True)
    async def reset_daily_command(self, ctx):
        reset_daily_pack()
        print('Reset Daily Pack status successfully.')
        await ctx.reply('🍔 Reset all **DailyPack** status successfully.')

    @reset_daily_command.error
    async def reset_daily_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('⚠ This commands only used in Admin role.')
    
    @commands.command(name='clear')
    @commands.has_permissions(manage_roles=True)
    async def clear_command(self, ctx, number: int):
        await ctx.reply(f'**{number}** message has been deleted.', mention_author=False)
        await ctx.channel.purge(limit=number + 1)

    @clear_command.error
    async def clear_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = 'You are missing the required premission to run this command!'
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f'Missing a required argument: {error.param}'
        else:
            message = "Something went wrong whlie running the commands"

        await ctx.reply(message, mention_author=False)

def setup(bot):
    bot.add_cog(Administrator(bot))
