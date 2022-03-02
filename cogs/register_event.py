import random
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mysql.connector import MySQLConnection, Error

from database.db_config import read_db_config

db = read_db_config()


def get_package_data(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT package_data FROM scum_package WHERE package_name = %s', (package_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


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


def update_mission(discord_id, status):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET MISSION = %s WHERE DISCORD_ID = %s', (status, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def event_register(discord_name, discord_id, steleport_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('INSERT INTO scum_wwii_event(DISCORD_NAME, DISCORD_ID, STEAM_ID) VALUES(%s,%s,%s)',
                    (discord_name, discord_id, steleport_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def select_teleport(discord_id, teleport):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET teleport = %s WHERE DISCORD_ID = %s', (teleport, discord_id,))
        conn.commit()
        cur.execute('SELECT teleport FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def event_count(teleport):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_wwii_event WHERE teleport = %s', (teleport,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def check_teleport(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT TELEPORT FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def add_to_cart(discord_id, discord_name, steleport_id, product_code, package_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_shopping_cart(discord_id, discord_name, steam_id, order_number, ' \
              'package_name) VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, discord_name, steleport_id, product_code, package_name,))
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
        conn = MySQLConnection(**db)
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
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(order_number) FROM scum_shopping_cart WHERE discord_id = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            order = list(row)
            return order[0]
    except Error as e:
        print(e)


def update_teleport(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET TELEPORT = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def update_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET STATUS = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def update_uniform_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET UNIFORM_SET = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def update_weapong_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET WEAPON_SET = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def check_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT STATUS FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def check_weapon_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT WEAPON_SET FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def check_uniform_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT UNIFORM_SET FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def team_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT TEAM FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


def players_event(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]

    except Error as e:
        print(e)


class EventRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        ww2_btn = interaction.component.custom_id
        player = players(member.id)
        teleport = check_teleport(member.id)
        team = team_check(member.id)
        status = check_status(member.id)
        weapon = check_weapon_status(member.id)
        uniform = check_uniform_status(member.id)
        cmd_channel = self.bot.get_channel(925559937323659274)
        run_cmd_channel = self.bot.get_channel(927796274676260944)
        event = players_event(member.id)
        message = None
        if ww2_btn == 'event_register':
            if player[11] == 0 and player[3] is not None:
                message = '🎉 ลงทะเบียนเข้าร่วมกิจกรรม WW2 EP2 สำเร็จ'
                status = 1
                update_mission(member.id, status)
                event_register(member.name, member.id, player[3])
                print('New players register event.')
            elif player[3] is None:
                message = 'คุณยังไม่ได้ทำการลงทะเบียน Steleport id'
            else:
                message = "⚠ Error, คุณได้ลงทะเบียนไว้แล้ว"
        elif ww2_btn == 'event_a':
            teleport = 'RED'
            select = select_teleport(member.id, teleport)
            count = event_count(teleport)
            message = f'{member.name} คุณได้เลือกทีม {select} จำนวนผู้เล่นในทีม ทั้งหมด {count}'
        elif ww2_btn == 'event_b':
            teleport = 'BLUE'
            select = select_teleport(member.id, teleport)
            count = event_count(teleport)
            message = f'{member.name} คุณได้เลือกทีม {select} จำนวนผู้เล่นในทีม ทั้งหมด {count}'
        elif ww2_btn == 'medicine':
            if teleport == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
            elif status == 0:
                message = '⚠ ขออภัยคุณได้รับเซ็ตอาวุธสำหรับกิจแล้ว'
            else:
                package = 'dailypack'
                code = random.randint(9, 99999)
                order_number = f'order{code}'
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง {package.upper()} ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                queue = check_queue()
                order = in_order(player[2])
                await cmd_channel.send(
                    f'{member.mention}'
                    f'```{package} id {order_number} delivery in progress from {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn == 'sniper':
            if teleport == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
            elif status == 0:
                message = '⚠ ขออภัยคุณได้รับเซ็ตอาวุธสำหรับกิจแล้ว'
            else:
                package = 'compound_woodland'
                code = random.randint(9, 99999)
                order_number = f'order{code}'
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง {package.upper()} ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                queue = check_queue()
                order = in_order(player[2])
                await cmd_channel.send(
                    f'{member.mention}'
                    f'```{package} id {order_number} delivery in progress from {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn == 'attacker':
            if teleport == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
            elif status == 0:
                message = '⚠ ขออภัยคุณได้รับเซ็ตอาวุธสำหรับกิจแล้ว'
            else:
                package = 'attacker_set'
                code = random.randint(9, 99999)
                order_number = f'order{code}'
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง {package.upper()} ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                queue = check_queue()
                order = in_order(player[2])
                await cmd_channel.send(
                    f'{member.mention}'
                    f'```{package} id {order_number} delivery in progress from {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn == 'uniform_red':
            if teleport == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
            elif status == 0:
                message = '⚠ ขออภัยคุณได้รับเซ็ตเครื่องแต่งกายสำหรับกิจแล้ว'
            elif team != event[4]:
                message = f'⚠ ขออภัยคุณ คุณต้องเลือกชุดของทีม {event[4]}'
            else:
                package = 'uniform_red'
                code = random.randint(9, 99999)
                order_number = f'order{code}'
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง {package.upper()} ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                queue = check_queue()
                order = in_order(player[2])
                await cmd_channel.send(
                    f'{member.mention}'
                    f'```{package} id {order_number} delivery in progress from {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn == 'teleport_blue':
            if teleport == 1:
                message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
                teleport = f'.set #teleport 584233.000 -84023.656 1666.030 {player[3]}'
                update_teleport(member.id)
                await run_cmd_channel.send(teleport)
                await run_cmd_channel.send(f'.location #Location {player[3]} true')

        elif ww2_btn == 'teleport_red':
            if teleport == 1:
                message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
                teleport = f'.set #teleport 589340.438 -127331.359 2079.710 {player[3]}'
                update_teleport(member.id)
                await run_cmd_channel.send(teleport)
                await run_cmd_channel.send(f'.location #Location {player[3]} true')

        elif ww2_btn == 'uniform_blue':
            if teleport == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
            elif status == 0:
                message = '⚠ ขออภัยคุณได้รับเซ็ตเครื่องแต่งกายสำหรับกิจแล้ว'
            elif team != event[4]:
                message = f'⚠ ขออภัยคุณ คุณต้องเลือกชุดของทีม {event[4]}'
            else:
                package = 'uniform_blue'
                code = random.randint(9, 99999)
                order_number = f'order{code}'
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง {package.upper()} ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                queue = check_queue()
                order = in_order(player[2])
                await cmd_channel.send(
                    f'{member.mention}'
                    f'```{package} id {order_number} delivery in progress from {order}/{queue}```'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        await interaction.respond(content=message)
        return

    @commands.command(name='ww2')
    async def ww2_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='REGISTER', emoji='📝', custom_id='event_register'),
                    Button(style=ButtonStyle.red, label='RED teleport', emoji='🛡', custom_id='event_a'),
                    Button(style=ButtonStyle.blue, label='BLUE teleport', emoji='⚔', custom_id='event_b')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='event_set')
    async def event_set_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle_l2.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='MEDICINE', emoji='💉', custom_id='medicine'),
                    Button(style=ButtonStyle.blue, label='SNIPER', emoji='🏹', custom_id='sniper'),
                    Button(style=ButtonStyle.red, label='ATTACKER', emoji='⚔', custom_id='attacker')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='event_uniform_set')
    async def event_uniform_set(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle_l.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label='UNIFORM RED', emoji='👔', custom_id='uniform_red'),
                    Button(style=ButtonStyle.blue, label='UNIFORM BLUE', emoji='👕', custom_id='uniform_blue')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='clears')
    async def clears_command(self, ctx, number: int):
        await ctx.send(f'Message **{number + 2}** has been deleted')
        await ctx.channel.purge(limit=number + 2)
    

    @commands.command(name='teleport')
    async def teleport_comamnd(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/teleport_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='GOTO TEAM BLUE', emoji='✈', custom_id='teleport_blue'),
                    Button(style=ButtonStyle.red, label='GOTO TEAM RED', emoji='✈', custom_id='teleport_red')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(EventRegister(bot))
