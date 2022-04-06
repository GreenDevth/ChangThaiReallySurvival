import asyncio
import random

import discord
import requests
from discord.ext import commands

from config.Auth import get_token

token = get_token(2)
url = get_token(3)

auth = f"{token}"
head = {'Authorization': 'Brarer' + auth}

response = requests.get('https://api.battlemetrics.com/servers/13458708')
print(response)
print(response.json()['data']['attributes']['players'])


def get_players():
    # res = requests.get(url, headers=head)
    player = response.json()['data']['attributes']['players']
    return player


class CountMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is online')
        while True:
            status_type = random.randint(0, 1)
            if status_type == 0:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f"ผู้รอดชีวิต {player}/20 คน"))
            else:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f'ผู้รอดชีวิต {player}/20 คน'))
            await asyncio.sleep(45)


def setup(bot):
    bot.add_cog(CountMembers(bot))
