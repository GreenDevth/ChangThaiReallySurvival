from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config
from db.players_db import players

db = read_db_config()


def get_guild_id(discord_id):
    """ Get Guild id from discord id """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT GUILD_ID FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_discord_id(guild_id):
    """ Get discord id from guild id """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT DISCORD_ID FROM scum_players WHERE GUILD_ID = %s'
        cur.execute(sql, (guild_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def update_coins(discord_id, amount):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'update scum_players set COINS = %s where DISCORD_ID = %s'
        cur.execute(sql, (amount, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
