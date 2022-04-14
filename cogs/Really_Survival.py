from discord.ext import commands
from extension.Task import MemberOnlineStatus
from extension.ManageMembers import JoinServer
from extension.ServerInformation import ServerInformation, RegisterMember
from extension.Players_Commands import PlayerCommand


class ReallySurvival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name + " Connected.")


def setup(bot):
    bot.add_cog(ReallySurvival(bot))
    bot.add_cog(MemberOnlineStatus(bot))
    bot.add_cog(JoinServer(bot))
    bot.add_cog(PlayerCommand(bot))
    bot.add_cog(ServerInformation(bot))
    bot.add_cog(RegisterMember(bot))
