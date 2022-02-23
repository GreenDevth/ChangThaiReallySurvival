import asyncio
import json
import random

import discord
import requests
from discord.ext import commands
from discord_components import Button, ButtonStyle
from db.Auth import get_token
from db.players_db import players, coins_update
from events.event_award import *

token = get_token(2)
url = get_token(3)
auth = f'{token}'
head = {'Authorization': 'Brarer' + auth}


class ZombieEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spawn_item')
    async def spawn_item_command(self, ctx):
        for x in spawn_box:
            box = random.choice(box_list)
            await ctx.channel.send(f'.set {box}"{x}"', mention_author=False)
            await asyncio.sleep(60)

    @commands.command(name='spawn_zombie')
    async def spawn_zombie_command(self, ctx):
        for x in zombie_location:
            zombies = random.choice(zombie_list)
            await ctx.channel.send(f'.set {zombies}"{x}"')
            await asyncio.sleep(10)

    @commands.command(name='spawn_zombie1')
    async def spawn_zombie1_command(self, ctx):
        for x in spawn_zombie:
            zombies = random.choice(zombie_list)
            await ctx.channel.send(f'.set {zombies}"{x}"')

            await asyncio.sleep(20)

    @commands.command(name='spawn_arrow')
    async def spawn_arrow_command(self, ctx):
        for x in zombie_location:
            arrow = arrow_item.pop(random.randrange(len(arrow_item)))
            await ctx.channel.send(f'.set {arrow}"{x}"')
            await asyncio.sleep(30)

    @commands.command(name='spawn_other')
    async def spawn_other_command(self, ctx):
        for x in spawn_zombie:
            other = spawn_item.pop(random.randrange(len(spawn_item)))
            # other = random.choice(spawn_item)
            await ctx.channel.send(f'.set {other}"{x}"')
            await asyncio.sleep(40)

    @commands.command(name='zombie_event')
    async def zombie_event(self, ctx):
        await ctx.channel.send(
            file=discord.File('./img/bank/event.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='Item', custom_id='spawn_item', emoji='🎁'),
                    Button(style=ButtonStyle.red, label='Zombie', custom_id='spawn_zombie', emoji='👻'),
                    Button(style=ButtonStyle.gray, label='Arrow', custom_id='spawn_arrow', emoji='🏹'),
                    Button(style=ButtonStyle.blue, label='Taxi', custom_id='spawn_teleport', emoji='🚘')
                ]
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        player = players(member.id)
        cmd_channel = self.bot.get_channel(927796274676260944)
        coin = player[5]
        player_coin = int(coin)
        fine = 500
        if event_btn == 'spawn_teleport' and player is not None:
            response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
            res_text = response.text
            json.loads(res_text)
            json_obj = response.json()
            game_time = json_obj['data']['attributes']['details']['time']
            open_time = "01:00"
            end_time = "05:00"
            if game_time <= end_time:
                if fine <= player_coin:
                    minus = player_coin - fine
                    print(player_coin - fine)
                    print(f'start event at {open_time} to {end_time} but game time at {game_time} , event time open.')
                    await interaction.respond(content='ระบบกำลังนำท่านมายังพื้นที่ล่าสมบัติ และหักค่าบริการ 500 เหรียญ')
                    await cmd_channel.send(f'.set #teleport 505213.656 594171.688 8094.190 {player[3]}')
                    coins_update(player[2], minus)

                if player_coin < 500:
                    await interaction.respond(content='ยอดเงินของคุณไม่เพียงพอสำหรับชำระค่าเข้าพื้นที่ล่าสมบัติ')
                    return
            if end_time <= game_time:
                print(end_time <= game_time)
                print(f'start event at {open_time} to {end_time} but game time at {game_time} , event time close.')
                await interaction.respond(content=f'เวลาในเกมส์ตอนนี้ {game_time} เป็นเวลากลางวัน และ Event ยังไม่เปิด')

        if event_btn == 'spawn_arrow' and player is not None:
            response = requests.get("https://api.battlemetrics.com/servers/13458708", headers=head)
            res_text = response.text
            json.loads(res_text)
            json_obj = response.json()
            game_time = json_obj['data']['attributes']['details']['time']
            open_time = "01:00"
            end_time = "05:00"
            if game_time <= end_time:
                print(f'start event at {open_time} to {end_time} but game time at {game_time} , event time open.')
                await interaction.respond(content='ระบบกำลังส่งอาวุธให้กับท่าน')
                print(f'{member.name} is click')
                for x in arrow_set:
                    await cmd_channel.send(f'.set {x}"505213.656 594171.688 8094.190"')
                    await asyncio.sleep(1)
                return
            if end_time <= game_time:
                print(end_time <= game_time)
                print(f'start event at {open_time} to {end_time} but game time at {game_time} , event time close.')
                await interaction.respond(content=f'เวลาในเกมส์ตอนนี้ {game_time} เป็นเวลากลางวัน และ Event ยังไม่เปิด')

        if event_btn == 'spawn_item':
            if interaction.author.id == 499914273049542677:
                await interaction.respond(content='เซ็ตอาวุธ จะเริ่มสุ่มดรอป ทุก ๆ 1 นาที')
                for x in box_list:
                    location = random.choice(spawn_box)
                    await cmd_channel.send(f'.set {x}"{location}"')
                    await asyncio.sleep(60)
                return
            else:
                await interaction.respond(content='สำหรับ admin เท่านั้น')

        if event_btn == 'spawn_zombie':
            if interaction.author.id == 499914273049542677:
                await interaction.respond(content='ซอมบี้ จะเริ่มสุ่มดรอป ทุก ๆ 10 วินาที')
                for x in zombie_location:
                    zombies = random.choice(zombie_list)
                    await cmd_channel.send(f'.set {zombies}"{x}"')
                    await asyncio.sleep(10)
                return
            else:
                await interaction.respond(content='สำหรับ admin เท่านั้น')


def setup(bot):
    bot.add_cog(ZombieEvent(bot))
