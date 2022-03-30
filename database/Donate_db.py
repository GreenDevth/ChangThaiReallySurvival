from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config
from datetime import datetime

db = read_db_config()


def donate_players(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_donate where discord_id=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def create_new_donate_member(discord, name, room, date):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('INSERT INTO scum_donate(discord_id, discord_name, room_name, donate_date) VALUES (%s,%s,%s,%s)',
                    (discord, name, room, date,))
        conn.commit()
        cur.close()
        print("New Donate Player Created...")
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return False


def get_donate_room(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select room_name from scum_donate where discord_id=%s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_players_id(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select PLAYERS_ID from scum_players where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def players_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_players where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def update_date(discord_id):
    now = datetime.now()
    date = now.strftime("%H:%M:%S")
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_donate set donate_date = %s where discord_id=%s', (date, discord_id,))
        conn.commit()
        cur.close()
        print("Donate date updated...")
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return False


def update_date_channel(discord_id, room):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_donate set room_name = %s where discord_id=%s', (room, discord_id,))
        conn.commit()
        cur.close()
        print("Donate room updated...")
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return False
