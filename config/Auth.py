import os

from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def get_token(arg):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select token from scum_discord_token where token_id = %s', (arg,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def load_cogs(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
