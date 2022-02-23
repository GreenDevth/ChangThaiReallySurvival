from discord.ext.commands import Cog
from discord.ext import commands

class ServerUtilities(Cog):
    def __init__(self, bot):
        self.bot = bot



    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply('*Your type unavailable commands*', mention_author=False)


def setup(bot):
    bot.add_cog(ServerUtilities(bot))