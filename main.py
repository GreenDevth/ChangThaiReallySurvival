import discord
from discord.ext import commands
from discord_components import DiscordComponents
from config.Auth import get_token, load_cogs

token = get_token(10)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
DiscordComponents(bot)

bot.load_extension('admin')
load_cogs(bot)
bot.run(token)
