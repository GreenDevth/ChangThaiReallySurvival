from mysql.connector import MySQLConnection,Error
from db.db_config import read_db_config
db = read_db_config()


def get_token(tokenid):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT token FROM scum_discord_token WHERE token_id = %s', (tokenid,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)