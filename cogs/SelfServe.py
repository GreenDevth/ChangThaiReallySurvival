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


class SelfServeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        store_btn = interaction.component.custom_id

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
                player = players(member.id)
                await interaction.respond(content='Daily Pack is being delivered to {}'.format(player[3]))
            else:
                await interaction.respond(content='⚠ Error, your account ID not found!')

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

    @commands.command(name='selfserve')
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

    @commands.command(name='server')
    async def server_command(self, ctx):
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

    @commands.command(name='bank')
    async def bank_command(self, ctx):
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

    @commands.command(name='dmbank')
    async def dmbank_command(self, ctx):
        check = players_exists(ctx.author.id)
        if check == 1:
            await ctx.reply('Please ured button in <#942256560120422512> for get private bank balance.',
                            mention_author=False)
        else:
            await ctx.reply('⚠ Error, your account ID not found!')

    @commands.command(name='daily')
    async def daily_command(self, ctx):
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
                    f'```Order number {order_number} delivery in progress from {order}/{queue}'
                )
                await run_cmd_channel.send('!checkout {}'.format(order_number))
            else:
                await ctx.reply('⚠ Error, your account ID not found!')
        elif time <= shop_open:
            await ctx.reply('Drone is still unavailable : the shop has been closed')

    @commands.command(name='status')
    async def status_command(self, ctx):
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


def setup(bot):
    bot.add_cog(SelfServeCommand(bot))
