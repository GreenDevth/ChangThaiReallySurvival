from database.db_config import *


def players_exists(discord_id):
    try:
        cxn = database
        cur = cxn.cursor()
        sql = 'SELECT COUNT(*) FROM scum_players WHERE discord_id = ?'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
        return None


def players(discord_id):
    try:
        cxn = database
        cur = cxn.cursor()
        sql = 'SELECT * FROM scum_players  WHERE discord_id = ?'
        cur.execute(sql, (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x

    except Error as e:
        print(e)


def players_register(player_name, discord_id, steam_id, bank_id):
    try:
        cxn = database
        cur = cxn.cursor()
        sql = 'INSERT INTO scum_players(players_name, discord_id, steam_id, bank_id) VALUES(?,?,?,?)'
        cur.execute(sql, (player_name, discord_id, steam_id, bank_id,))
        cxn.commit()
        cur.close()
    except Error as e:
        print(e)


def transfer_player(member_name, member_discord, member_steam, member_level, member_exp, member_bank, member_coins):
    try:
        cxn = database
        cur = cxn.cursor()
        sql = 'INSERT INTO scum_players(players_name, discord_id, steam_id, exp, level, member, daily_pack, special, bank_id, coins) VALUES(?,?,?,?,?,?,?,?,?,?)'
        cur.execute(sql, (member_name, member_discord, member_steam, member_level, member_exp, member_bank, member_coins, "player", 1, 1,))
        cxn.commit()
        cur.close()
    except Error as e:
        print(e)