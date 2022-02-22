import os
import sqlite3
from sqlite3 import Error
from configparser import ConfigParser


def read_db_config(filename='config.ini', section="mysql"):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


database = sqlite3.connect("./database/scum_players.db")
cursor = database.cursor()


def get_token(name):
    try:
        cxn = database
        cur = cxn.cursor()
        sql = 'SELECT token FROM discord_token WHERE bot_name = ?'
        cur.execute(sql, (name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def cogs(bot):
    for filename in os.listdir('./extension'):
        if filename.endswith('.py'):
            bot.load_extension(f'extension.{filename[:-3]}')
