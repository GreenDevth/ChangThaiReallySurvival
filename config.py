import os


def cogs(bot):
    for filename in os.listdir('./extension'):
        if filename.endswith('.py'):
            bot.load_exetension(f'extension.{filename[:-3]}')
