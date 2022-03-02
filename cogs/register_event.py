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


def event_register(discord_name, discord_id, steam_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('INSERT INTO scum_wwii_event(DISCORD_NAME, DISCORD_ID, STEAM_ID) VALUES(%s,%s,%s)',
                    (discord_name, discord_id, steam_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def select_team(discord_id, team):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_wwii_event SET TEAM = %s WHERE DISCORD_ID = %s', (team, discord_id,))
        conn.commit()
        cur.execute('SELECT TEAM FROM scum_wwii_event WHERE DISCORD_ID = %s', (discord_id,))
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


def event_count(team):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_wwii_event WHERE TEAM = %s', (team,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def check_team_information(discord_id):
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


def add_to_cart(discord_id, discord_name, steam_id, product_code, package_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_shopping_cart(discord_id, discord_name, steam_id, order_number, ' \
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


class EventRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        ww2_btn = interaction.component.custom_id
        player = players(member.id)
        team = check_team_information(member.id)
        cmd_channel = self.bot.get_channel(925559937323659274)
        run_cmd_channel = self.bot.get_channel(927796274676260944)
        message = None
        if ww2_btn == 'event_register':
            if player[11] == 0 and player[3] is not None:
                message = '🎉 ลงทะเบียนเข้าร่วมกิจกรรม WW2 EP2 สำเร็จ'
                status = 1
                update_mission(member.id, status)
                event_register(member.name, member.id, player[3])
                print('New players register event.')
            elif player[3] is None:
                message = 'คุณยังไม่ได้ทำการลงทะเบียน Steam id'
            else:
                message = "⚠ Error, คุณได้ลงทะเบียนไว้แล้ว"
        elif ww2_btn == 'event_a':
            team = 'RED'
            select = select_team(member.id, team)
            count = event_count(team)
            message = f'{member.name} คุณได้เลือกทีม {select} จำนวนผู้เล่นในทีม ทั้งหมด {count}'
            print(message)
        elif ww2_btn == 'event_b':
            team = 'BLUE'
            select = select_team(member.id, team)
            count = event_count(team)
            message = f'{member.name} คุณได้เลือกทีม {select} จำนวนผู้เล่นในทีม ทั้งหมด {count}'
            print(message)
        elif ww2_btn == 'medicine':
            if team == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
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
            if team == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
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
            if team == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
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
            if team == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
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
        elif ww2_btn == 'uniform_blue':
            if team == 1:
                message = '⚠ ขอภัยคุณอยู่นอกพื้นที่กิจกรรม'
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
        await interaction.respond(content=message, ephemeral=False)
        return

    @commands.command(name='ww2')
    async def ww2_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='REGISTER', emoji='📝', custom_id='event_register'),
                    Button(style=ButtonStyle.red, label='RED TEAM', emoji='🛡', custom_id='event_a'),
                    Button(style=ButtonStyle.blue, label='BLUE TEAM', emoji='⚔', custom_id='event_b')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='event_set')
    async def event_set_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle.png'),
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
            file=discord.File('./img/event/the_battle.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label='UNIFORM RED', emoji='👔', custom_id='uniform_red'),
                    Button(style=ButtonStyle.blue, label='UNIFORM BLUE', emoji='👕', custom_id='uniform_blue')
                ]
            ]
        )

    @commands.command(name='clear')
    async def clear_command(self, ctx, number: int):
        await ctx.send(f'Message **{number + 2}** has been deleted')
        await ctx.channel.purge(limit=number + 2)


def setup(bot):
    bot.add_cog(EventRegister(bot))
