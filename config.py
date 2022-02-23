import os


def cogs(bot):
    for filename in os.listdir('./extension'):
        if filename.endswith('.py'):
            bot.load_extension(f'extension.{filename[:-3]}')
