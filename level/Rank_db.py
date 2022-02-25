from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def player_rank():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT DISCORD_NAME, LEVEL, EXP FROM scum_players WHERE EXP > 0 ORDER BY EXP DESC LIMIT 5')
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)
