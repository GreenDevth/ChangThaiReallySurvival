import random
from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def new_player(name, discord, guild, join_date):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_players(DISCORD_NAME, DISCORD_ID, GUILD_ID, CREATE_DATE) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (name, discord, guild, join_date))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            msg = "โปรดเตรียม สตรีมไอดี สำหรับลงทะเบียนและรับรหัสปลดล็อคจากเซิร์ฟ"
            return msg.strip()


def player_info(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x

    except Error as e:
        print(e)


def remove_player(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('DELETE FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return e
    finally:
        if conn.is_connected():
            conn.close()
            return None


def member_check(discord_id):
    """ Return 0 when found members or 1 when not found members """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scum_players WHERE DISCORD_ID=%s", (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)

def steam_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT STEAM_ID FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def generate_code(length):
    string_code = 'reallysurvival'
    result = ''.join((random.choice(string_code)) for x in range(length))
    return result.upper()

def update_steam_id(discord_id, steam_id, activatecode):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET STEAM_ID = %s, ACTIVATE_CODE = %s WHERE DISCORD_ID = %s',
                    (steam_id, activatecode, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()

def verify_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select VERIFY from scum_players where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def activate_code_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select ACTIVATE_CODE from scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        return None
    except Error as e:
        print(e)


def activate_code(activatecode):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET VERIFY = 1 WHERE ACTIVATE_CODE = %s', (activatecode,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            msg = "Activate successfull: โปรดรอข้อความตอบกลับจากเซิร์ฟอีกครั้ง เมื่อระบบทำการปรับสถานะของคุณเรียบร้อยแล้ว"
            return msg.strip()

def update_to_exclusive(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute("UPDATE scum_players SET MEMBER='exclusive' WHERE DISCORD_ID=%s", (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return e
    finally:
        if conn.is_connected():
            conn.close()
            msg = "update successfull"
            return msg.strip()