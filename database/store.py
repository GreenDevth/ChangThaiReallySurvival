from database.db_config import *

def in_order():
    try:
        conn = database
        cur = conn.cursor()
        sql = 'SELECT COUNT(*) FROM shopping_cart'
        cur.execute(sql)
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
        
        
def add_to_cart(discord_name, steam_id, order_code, package_name):
    try:
        conn = database
        cur = conn.cursor()
        sql = 'INSERT INTO shopping_cart(discord_name, steam_id, order_code, package_name) VALUES(?,?,?,?)'
        cur.execute(sql, (discord_name, steam_id, order_code, package_name,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)