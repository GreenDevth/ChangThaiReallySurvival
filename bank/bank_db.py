from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def update_coins(amount, discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s', (amount, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
