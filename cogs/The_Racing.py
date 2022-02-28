import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from events.events_db import *
from store.store_db import add_to_cart, in_order, check_queue


class RacingEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        total = count_event_player()
        check = players_exists(member.id)
        message = None
        if event_btn == "racing_register":
            if check == 0:
                message = "คุณได้ลงทะเบียนเป็นที่เรียบร้อย"
                steam_id = get_steam_id(member.id)
                new_players_event(member.name, member.id, steam_id)
                totals = count_event_player()
                await interaction.edit_origin(
                    components=[
                        [
                            Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                            Button(style=ButtonStyle.green, label=f'NUMBER OF REGISTERED PLAYERS : {totals}',
                                   emoji='📝',
                                   custom_id='racing_count', disabled=False),
                        ]
                    ]
                )
                await interaction.channel.send(message, delete_after=5)
                return
            else:
                await interaction.edit_origin(
                    components=[
                        [
                            Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                            Button(style=ButtonStyle.green, label=f'NUMBER OF REGISTERED PLAYERS : {total}', emoji='📝',
                                   custom_id='racing_count', disabled=False),
                        ]
                    ]
                )
                await interaction.channel.send("📢 คุณได้ลงทะเบียนไว้แล้ว", delete_after=5)
                return

        elif event_btn == "racing_count":
            await interaction.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                        Button(style=ButtonStyle.green, label=f'NUMBER OF REGISTERED PLAYERS : {total}', emoji='📝',
                               custom_id='racing_count', disabled=False),
                    ]
                ]
            )

        elif check == 1:
            message = None
            player = get_players_event(member.id)
            code = random.randint(9, 99999)
            order_number = f'order{code}'
            cmd_channel = self.bot.get_channel(925559937323659274)
            run_cmd_channel = self.bot.get_channel(927796274676260944)
            if event_btn == 'set_a':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'set_b':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'set_c':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'set_d':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'set_e':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'bike_a':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'bike_b':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'bike_c':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            elif event_btn == 'bike_d':
                package_name = f'bike_event_{event_btn}'
                message = f'{member.name} คำสั่งหมายเลข {order_number} ระบบกำลังเตรียมจัดส่งไปให้คุณ โปรดรอสักครู่'
                add_to_cart(player[2], player[1], player[3], order_number, package_name)
                queue = check_queue()
                order = in_order(player[2])
                update_event_status(player[2])
                await cmd_channel.send(
                    f'{member.mention} ```Order number {order_number} delivery in progress from {order}/{queue}```')
                await run_cmd_channel.send('!checkout {}'.format(order_number))

            await interaction.respond(content=message)
            return

    @commands.command(name='uniform_set')
    async def uniform_set_command(self, ctx):
        uniform = [
            "set_a",
            "set_b",
            "set_c",
            "set_d",
            "set_e"

        ]
        bike = [
            "bike_a",
            "bike_b",
            "bike_c",
            "bike_d"
        ]
        random_bike = random.choice(bike)
        random_uniform = random.choice(uniform)
        await ctx.send(
            file=discord.File('./img/event/the_racing.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET UNIFORM', emoji='🥋', custom_id=random_uniform),
                    Button(style=ButtonStyle.red, label='GET MOUNTAIN BIKE', emoji='🚴‍', custom_id=random_bike)
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='racing')
    async def racing_command(self, ctx):
        total = count_event_player()
        await ctx.send(
            file=discord.File('./img/event/the_racing.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                    Button(style=ButtonStyle.red, label=f'NUMBER OF REGISTERED PLAYERS : {total}', emoji='📝',
                           custom_id='racing_count', disabled=False),
                ]
            ]
        )


def setup(bot):
    bot.add_cog(RacingEvent(bot))
