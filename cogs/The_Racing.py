import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from events.events_db import *


class RacingEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        total = count_event_player()
        message = None
        if event_btn == "racing_register":
            message = "คุณได้ลงทะเบียนเป็นที่เรียบร้อย"
            await interaction.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                        Button(style=ButtonStyle.red, label=f'NUMBER OF REGISTERED PLAYERS : {total}', emoji='📝',
                               custom_id='racing_count', disabled=True),
                    ]
                ]
            )
        await interaction.respond(content=message)

    @commands.command(name='racing')
    async def racing_command(self, ctx):
        total = count_event_player()
        await ctx.send(
            file=discord.File('./img/event/bike2.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                    Button(style=ButtonStyle.red, label=f'NUMBER OF REGISTERED PLAYERS : {total}', emoji='📝',
                           custom_id='racing_count', disabled=True),
                ]
            ]
        )


def setup(bot):
    bot.add_cog(RacingEvent(bot))
