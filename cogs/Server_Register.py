from discord.ext import commands


class PlayerRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reg')
    async def player_reg_command(self, ctx, steam_id: int):
        await ctx.reply('Register Successfully..')

    @player_reg_command.error
    async def player_reg_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('')


def setup(bot):
    bot.add_cog(PlayerRegister(bot))
