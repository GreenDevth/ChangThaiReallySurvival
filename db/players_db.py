from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def players(discord_id):
    """ Get All information players. """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def new_players(name, discord, steam, guild):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_players(DISCORD_NAME, DISCORD_ID, STEAM_ID, GUILD_ID) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (name, discord, steam, guild,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def exp_up(discord_id, amount):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET EXP = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (amount, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def level_up(discord_id, amount):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET LEVEL = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (amount, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def coins_update(discord_id, amount):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (amount, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def remove_players(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('DELETE FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()