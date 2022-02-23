import discord
from discord.ext import commands
from discord_components import DiscordComponents
from database.db_config import *

token = get_token("really survival")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)
DiscordComponents(bot)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

cogs(bot)
bot.run(token)
