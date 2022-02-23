from discord.ext import commands
from discord_components import Button, ButtonStyle


class MissionVegetable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(MissionVegetable(bot))
