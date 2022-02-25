from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def player_rank():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT DISCORD_NAME, LEVEL, EXP FROM scum_players WHERE EXP > 0 ORDER BY EXP DESC LIMIT 5')
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
