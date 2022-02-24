from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def get_data(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT package_data FROM scum_package WHERE package_name = %s', (package_name,))
        row = cur.fetchone()
        while row is not None:
            return row
    except Error as e:
        print(e)


def add_to_cart(discord_id, discord_name, steam_id, product_code, package_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_shopping_cart(discord_id, discord_name, steam_id, product_code, ' \
              'package_name) VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, discord_name, steam_id, product_code, package_name,))
        print('Insert new order name {}'.format(product_code))
        conn.commit()
        cur.close()

    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def check_queue():
    """Count Queue for Shopping Cart"""
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_shopping_cart')
        row = cur.fetchone()
        while row is None:
            queue = 0
            return queue
        while row is not None:
            queue = list(row)
            return queue[0]
    except Error as e:
        print(e)


def in_order(discord_id):
    """Count product_code from current discord id"""
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(product_code) FROM scum_shopping_cart WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            order = list(row)
            return order[0]
    except Error as e:
        print(e)


def checkout(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COUNT(steam_id) FROM scum_shopping_cart WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_command(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT package_data FROM scum_package WHERE package_name = %s'
        cur.execute(sql, (package_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)