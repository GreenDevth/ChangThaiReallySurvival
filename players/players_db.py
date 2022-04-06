from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def new_players(name, discord, guild, join_date):
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
    finally:
        if conn.is_connected():
            conn.close()


def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select COUNT(*) from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def player_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def get_player_coins(discord_id):
    if player_check(discord_id) == 1:
        try:
            conn = MySQLConnection(**db)
            cur = conn.cursor()
            cur.execute('SELECT COINS FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
            row = cur.fetchone()
            res = list(row)
            return res[0]
        except Error as e:
            print(e)
    else:
        msg = "ไม่พบข้อมูลผู้ใช้งานในระบบ"
        return msg.strip()


def players(discord_id):
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


def players_bank(bank_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select COINS from scum_players where GUILD_ID = %s', (bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players_discord(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select GUILD_ID from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def update_daily_pack(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET DAILY_PACK = 0 WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)


def reset_daily_pack():
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET DAILY_PACK = 1 WHERE PLAYERS_ID > 0')
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


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


def exclusive_count():
    arg = "exclusive"
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(MEMBER) FROM scum_players WHERE MEMBER = %s', (arg,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def exclusive_update(discordid):
    conn = None
    arg = "exclusive"
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET MEMBER = %s WHERE DISCORD_ID = %s', (arg, discordid,))
        conn.commit()
        print('Update successfully...')
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_discord_id(by_bank_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select DISCORD_ID from scum_players WHERE GUILD_ID = %s', (by_bank_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def update_player_coins(discord_id, amount):
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
            return None
