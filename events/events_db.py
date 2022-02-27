from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_events WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def new_players_event(discord_name, discord_id, steam_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('INSERT INTO scum_events(DISCORD_NAME, DISCORD_ID, STEAM_ID) VALUES (%s,%s,%s)',
                    (discord_name, discord_id, steam_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()