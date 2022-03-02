from discord.ext import commands
from discord_components import Button, ButtonStyle
import discord

from players.players_db import *


class EventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        player = players(member.id)
        cmd_channel = self.bot.get_channel(927796274676260944)
        ebtn = interaction.component.custom_id
        message = None

        if ebtn == 'teleport_blue':
            message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
            teleport = f'.set #teleport 584233.000 -84023.656 1666.030 {player[3]}'
            await cmd_channel.send(teleport)
            await cmd_channel.send(f'.location #Location {player[3]} true')
        elif ebtn == 'teleport_blue':
            message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
            teleport = f'.set #teleport =589340.438 -127331.359 2079.710 {player[3]}'
            await cmd_channel.send(teleport)
            await cmd_channel.send(f'.location #Location {player[3]} true')
        await interaction.respond(content=message)

    @commands.command(name='teleport')
    async def teleport_comamnd(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/teleport_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='TELEPORT BLUE', emoji='✈', custom_id='teleport_blue'),
                    Button(style=ButtonStyle.red, label='TELEPORT RED', emoji='✈', custom_id='teleport_red')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(EventCommand(bot))
