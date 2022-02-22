from discord.ext import commands
from database.store import in_order


class ServerStore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='in_order')
    async def in_order_command(self, ctx):
        check_in_order = in_order()
        await ctx.reply(f'{check_in_order}', mention_author=False)


def setup(bot):
    bot.add_cog(ServerStore(bot))
