import asyncio
import json
import random
from datetime import datetime

import discord
import requests
from discord.ext import commands
from discord_components import Button, ButtonStyle

from config.Auth import get_token
from players.players_db import players_exists, players, update_daily_pack
from store.store_db import add_to_cart, in_order, check_queue

token = get_token(2)
url = get_token(3)

auth = f"{token}"
head = {'Authorization': 'Brarer' + auth}


def get_players():
    res = requests.get(url, headers=head)
    player = res.json()['data']['attributes']['players']
    return player


class SelfServeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is online')
        while True:
            status_type = random.randint(0, 1)
            if status_type == 0:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f"ผู้รอดชีวิต {player}/20 คน"))
            else:
                player = get_players()
                print(player)
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f'ผู้รอดชีวิต {player}/20 คน'))
            await asyncio.sleep(45)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        store_btn = interaction.component.custom_id
        cmd_channel = self.bot.get_channel(925559937323659274)
        run_cmd_channel = self.bot.get_channel(927796274676260944)
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        shop_open = "18:00:00"

        if store_btn == 'server':
            response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
            res_text = response.text
            json.loads(res_text)
            json_obj = response.json()
            scum_server = json_obj['data']['attributes']['name']
            scum_ip = json_obj['data']['attributes']['ip']
            scum_port = json_obj['data']['attributes']['port']
            scum_player = json_obj['data']['attributes']['players']
            scum_player_max = json_obj['data']['attributes']['maxPlayers']
            scum_rank = json_obj['data']['attributes']['rank']
            scum_status = json_obj['data']['attributes']['status']
            scum_time = json_obj['data']['attributes']['details']['time']
            scum_version = json_obj['data']['attributes']['details']['version']
            await interaction.respond(
                content=f"```\nServer: {scum_server} "
                        f"\nIP: {scum_ip}:{scum_port} "
                        f"\nStatus: {scum_status} "
                        f"\nTime in Game: {scum_time} "
                        f"\nPlayers: {scum_player}/{scum_player_max} "
                        f"\nRanking: #{scum_rank} "
                        f"\nGame version: {scum_version}\n "
                        f"\nServer Restarts Every 6 hours "
                        f"\nDay 3.8 hours, Night 1 hours\n```",
            )
        elif store_btn == 'bankstatement':
            check = players_exists(member.id)
            if check == 1:
                player = players(member.id)
                coins = "${:,d}".format(player[5])
                await interaction.respond(
                    content=f'Account name : {player[1]}\n'
                            f'Bank ID : {player[4]}\n'
                            f'Bank Balance : {coins}'
                )
            else:
                await interaction.respond(content='⚠ Error, your account ID not found!')

        elif store_btn == 'dailypack':
            check = players_exists(member.id)
            if check == 1:
                if shop_open <= time:
                    player = players(member.id)
                    daily_pack = player[8]
                    if daily_pack == 1:
                        package_name = "dailypack"
                        code = random.randint(9, 99999)
                        order_number = f'order{code}'
                        await interaction.respond(content='Daily Pack is being delevered to {}'.format(player[3]))
                        add_to_cart(player[2], player[1], player[3], order_number, package_name)
                        queue = check_queue()
                        order = in_order(player[2])
                        update_daily_pack(player[2])
                        await cmd_channel.send(
                            f'{member.mention}'
                            f'```Order number {order_number} delivery in progress from {order}/{queue}```'
                        )
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                        return
                    elif daily_pack == 0:
                        message = '⚠ Error, Wait for get daily pack tomorrow.'
                        await interaction.respond(content=message)
                        return
                    else:
                        pass
                    return
                elif time <= shop_open:
                    await interaction.respond(
                        content='Drone is still unavailable : the shop has been closed, Shop open is 18:00 - 24:00')
                    return
            elif check == 0:
                await interaction.respond(content=check)
                return
            return

        elif store_btn == "status":
            check = players_exists(member.id)
            if check == 1:
                player = players(member.id)
                coins = "${:,d}".format(player[5])
                created_at = member.created_at.strftime("%b %d, %Y")
                joined_at = member.joined_at.strftime("%b %d, %Y")
                await interaction.respond(
                    content="```css\nYOU INFORMATION\n"
                            "=========================================================\n"
                            f"Discord Name : '{player[1]}'\n"
                            f"Discord ID : {player[2]}\n"
                            f"Steam ID : {player[3]}\n"
                            f"Bank ID : {player[4]}\n"
                            f"Bank Balance : {coins}\n"
                            f"Level : {player[6]}\n"
                            f"Exp : {player[7]}\n"
                            f"Join server at : '{joined_at}'\n"
                            "=========================================================\n"
                            "\n```"
                )
            else:
                await interaction.respond(content='⚠ Error, your account ID not found!')

        elif store_btn == 'get_ip':
            await interaction.edit_origin(
                components=[Button(style=ButtonStyle.red, label='Get IP/PWD', emoji='💻', custom_id='get_ip')]
            )
            await discord.DMChannel.send(member, 'ไอพีเซิร์ฟ : **143.244.33.48:7102**  รหัสผ่าน : **28702**')
            return
        return

    @commands.command(name='selfserve')
    @commands.has_permissions(manage_roles=True)
    async def selfserve_command(self, ctx):
        emoji = discord.utils.get(self.bot.emojis, name='ctrs')
        await ctx.send(
            f"{emoji} ChangThai℠ Really Survival",
            components=[
                [
                    Button(style=ButtonStyle.gray, label='Bank Statement', emoji='🏦', custom_id='bankstatement'),
                    Button(style=ButtonStyle.gray, label='Daily Pack', emoji='🍔', custom_id='dailypack'),
                    Button(style=ButtonStyle.gray, label='Sever Status', emoji='🌐', custom_id='server'),
                    Button(style=ButtonStyle.gray, label='Player Status', emoji='⚙', custom_id='status')
                ]
            ]
        )

    @selfserve_command.error
    async def selfserve_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('⚠ Error, **For Admin only**')

    @commands.command(name='server')
    @commands.has_role("Verify Members")
    async def server_command(self, ctx):
        cmd_channel = discord.utils.get(self.bot.get_all_channels(), id=925559937323659274)
        response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
        res_text = response.text
        json.loads(res_text)
        json_obj = response.json()
        scum_server = json_obj['data']['attributes']['name']
        scum_ip = json_obj['data']['attributes']['ip']
        scum_port = json_obj['data']['attributes']['port']
        scum_player = json_obj['data']['attributes']['players']
        scum_player_max = json_obj['data']['attributes']['maxPlayers']
        scum_rank = json_obj['data']['attributes']['rank']
        scum_status = json_obj['data']['attributes']['status']
        scum_time = json_obj['data']['attributes']['details']['time']
        scum_version = json_obj['data']['attributes']['details']['version']
        if cmd_channel == ctx.channel.id or ctx.author.guild_permissions.administrator:
            await ctx.reply(
                "```============================================="
                f"\nServer: {scum_server} "
                f"\nIP: {scum_ip}:{scum_port} "
                f"\nStatus: {scum_status} "
                f"\nTime in Game: {scum_time} "
                f"\nPlayers: {scum_player}/{scum_player_max} "
                f"\nRanking: #{scum_rank} "
                f"\nGame version: {scum_version}\n "
                f"\nServer Restarts Every 6 hours "
                f"\nDay 3.8 hours, Night 1 hours\n"
                f"=============================================```",
                mention_author=False
            )
        else:
            await ctx.reply('Please type this command in <#925559937323659274>')

    @server_command.error
    async def server_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#950952899519868978>',
                            mention_author=False)

    @commands.command(name='bank')
    @commands.has_role("Verify Members")
    async def bank_command(self, ctx):
        cmd_channel = discord.utils.get(self.bot.get_all_channels(), id=925559937323659274)
        if cmd_channel == ctx.channel.id or ctx.author.guild_permissions.administrator:
            check = players_exists(ctx.author.id)
            if check == 1:
                player = players(ctx.author.id)
                coins = "${:,d}".format(player[5])
                await ctx.reply(
                    '```css\n'
                    f'Account name : "{player[1]}", '
                    f'Bank ID : {player[4]}, '
                    f'Bank Balance : {coins}'
                    '\n```',
                    mention_author=False
                )
            else:
                await ctx.reply('⚠ Error, your account ID not found!')
        else:
            await ctx.reply('Please type this command in <#925559937323659274>')

    @bank_command.error
    async def bank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#950952899519868978>',
                            mention_author=False)

    @commands.command(name='dmbank')
    @commands.has_role("Verify Members")
    async def dmbank_command(self, ctx):
        cmd_channel = discord.utils.get(self.bot.get_all_channels(), id=925559937323659274)
        if ctx.channel.id != 925559937323659274:
            member = ctx.author
            check = players_exists(ctx.author.id)
            if check == 1:
                player = players(member.id)
                coins = "${:,d}".format(player[5])
                await discord.DMChannel.send(
                    member,
                    f'Account Name : {player[1]}\n'
                    f'Bank ID : {player[4]}\n'
                    f'Bank Balance : {coins}'
                )
                await ctx.reply('Bank statements are being delivered to your inbox.',
                                mention_author=False)
            else:
                await ctx.reply('⚠ Error, your account ID not found!')
        else:
            await ctx.reply('Please type this command in <#925559937323659274>')

    @dmbank_command.error
    async def dmbank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#950952899519868978>',
                            mention_author=False)

    @commands.command(name='daily')
    @commands.has_role("Verify Members")
    async def daily_command(self, ctx):
        cmd_channel = discord.utils.get(self.bot.get_all_channels(), id=925559937323659274)
        if cmd_channel == ctx.channel.id or ctx.author.guild_permissions.administrator:
            member = ctx.author
            cmd_channel = self.bot.get_channel(925559937323659274)
            run_cmd_channel = self.bot.get_channel(927796274676260944)
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            shop_open = "18:00:00"
            if shop_open <= time:
                check = players_exists(ctx.author.id)
                if check == 1:
                    player = players(ctx.author.id)
                    daily_pack = player[8]
                    if daily_pack == 1:
                        package_name = "dailypack"
                        code = random.randint(9, 999999)
                        order_number = f'order{code}'
                        await ctx.reply(
                            'Daily Pack is being delivered to {}'.format(player[3]), mention_author=False
                        )
                        add_to_cart(player[2], player[1], player[3], order_number, package_name)
                        queue = check_queue()
                        order = in_order(player[2])
                        update_daily_pack(player[2])
                        await cmd_channel.send(
                            f'{member.mention}'
                            f'```Order number {order_number} delivery in progress from {order}/{queue}```'
                        )
                        await run_cmd_channel.send('!checkout {}'.format(order_number))
                    else:
                        await ctx.reply('⚠ Error, Wait for get daily pack tomorrow.')
                else:
                    await ctx.reply('⚠ Error, your account ID not found!')
            elif time <= shop_open:
                await ctx.reply('Drone is still unavailable : the shop has been closed, Shop open is 18:00 - 24:00',
                                mention_author=False)
        else:
            await ctx.reply('Please type this command in <#925559937323659274>')

    @daily_command.error
    async def daily_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#950952899519868978>',
                            mention_author=False)

    @commands.command(name='status')
    @commands.has_role("Verify Members")
    async def status_command(self, ctx):
        cmd_channel = discord.utils.get(self.bot.get_all_channels(), id=925559937323659274)
        if cmd_channel == ctx.channel.id or ctx.author.guild_permissions.administrator:
            member = ctx.author
            check = players_exists(member.id)
            if check == 1:
                player = players(member.id)
                coins = "${:,d}".format(player[5])
                created_at = member.created_at.strftime("%b %d, %Y")
                joined_at = member.joined_at.strftime("%b %d, %Y")
                await ctx.reply(
                    content="```YOU INFORMATION\n"
                            "=========================================================\n"
                            f"Discord Name : '{player[1]}'\n"
                            f"Discord ID : {player[2]}\n"
                            f"Steam ID : {player[3]}\n"
                            f"Bank ID : {player[4]}\n"
                            f"Bank Balance : {coins}\n"
                            f"Level : {player[6]}\n"
                            f"Exp : {player[7]}\n"
                            f"Join server at : '{joined_at}'\n"
                            "========================================================="
                            "\n```",
                    mention_author=False
                )
            else:
                await ctx.reply(content='⚠ Error, your account ID not found!')
        else:
            await ctx.reply('Please type this command in <#925559937323659274>')

    @status_command.error
    async def status_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#950952899519868978>',
                            mention_author=False)

    @commands.command(name='get_ip')
    @commands.has_permissions(manage_roles=True)
    async def get_ip_commands(self, ctx):
        await ctx.send(
            file=discord.File('./img/banner.png')
        )
        await ctx.send(
            '⚔ **ChangThai℠ Really survival**\n'
            '\n- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 30 '
            '\n- อัตราการดรอปของเท่ากับ 1 เท่า ซอมบี้ดาเมจ 1 เท่า'
            '\n- ไม่มีกฎ ผู้เล่นสามารถทำอะไรได้เท่าที่เซิร์ฟตั้งค่าไว้'
            '\n- ยานพาหนะไม่มีดรอป ทำภารกิจเพื่อรับรถ หรือใช้เหรียญที่มีแลกซื้อได้'
            '\n- แอดมินจะช่วยเหลือเท่าที่สามารถทำได้ เฉพาะเวลาที่ออนไลน์เท่านั้น'
            '\n- จำกัด ผู้เล่นละ 1 ธงเท่านั้น จะทำการตรวจสอบธงทุกวันหากมีธงแต่ไม่มีสิ่งปลูกสร้างจะทำลายทิ้งทันที'
            '\n- ไม่แสดงแผนที่ เพิ่มความเสียหายช๊อตไฟฟ้า 50 เท่า'
            '\n- ไม่สามารถวางกับดักได้ ไม่มีการแสดงรายชื่อผู้ถูกสังหารและผู้สังหาร'
            '\n- สร้างบ้านได้ทุกที่ แต่ห้ามใช้บัคของเกมส์ในการก่อสร้าง เช่น รั้ว และตัวบ้าน\n'
            '\nกดรับ ไอพีและรหัสได้จากปุ่มด้านล่าง',
            components=[Button(style=ButtonStyle.red, label='Get IP/PWD', emoji='💻', custom_id='get_ip')]
        )

    @get_ip_commands.error
    async def get_ip_commands_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('⚠ Error, **For Admin only**')


def setup(bot):
    bot.add_cog(SelfServeCommand(bot))
