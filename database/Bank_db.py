from cgitb import reset
from database.db_config import *


def coins(bank_id):
    """ Get player coin from bank_id """
    try:
        conn = database
        cur = conn.cursor()
        sql = 'SELECT coins, discord_id FROM scum_players WHERE bank_id = ?'
        cur.execute(sql, (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res
    except Error as e:
        print(e)


def get_coins(discord_id):
    """ Get player coin with discord id """
    try:
        conn = database
        cur = conn.cursor()
        cur.execute('SELECT coins FROM scum_players WHERE discord_id = ?', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def update_coins(amount, member_id):
    try:
        conn = database
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET coins = ? WHERE discord_id = ?'
        cur.execute(sql, (amount, member_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
