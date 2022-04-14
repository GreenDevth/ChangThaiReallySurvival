import discord
import requests
from discord.ext import commands, tasks


class MemberOnlineStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_presence.start()

    @tasks.loop(seconds=10)
    async def change_presence(self):
        def get_players():
            try:
                response = requests.get('https://api.battlemetrics.com/servers/13458708')
                status = response.status_code
                if status == 200:
                    print(response.json()['data']['attributes']['players'])
                    player = response.json()['data']['attributes']['players']
                    return player
                else:
                    return 0
            except Exception as e:
                print(e)
                return 0

        result = f"{get_players()}/20 Prisoner"
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=result)
        )
