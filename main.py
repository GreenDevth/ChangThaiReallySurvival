import discord
from discord.ext import commands
from discord_components import DiscordComponents
from db.Auth import get_token
from config import cogs

token = get_token(10)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
DiscordComponents(bot)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


cogs(bot)
bot.run(token)
