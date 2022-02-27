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
        message = None
        if event_btn == "racing_register":
            message = "Create new event players"
        elif event_btn == "reacing_count":
            message = "Count event players"
        await interaction.respond(content=message)

    @commands.command(name='racing')
    async def racing_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/bike2.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='REGISTER', emoji='📝', custom_id='racing_register'),
                    Button(style=ButtonStyle.red, label='NUMBER OF REGISTERED PLAYERS : {}', emoji='📝',
                           custom_id='racing_count'),
                ]
            ]
        )


def setup(bot):
    bot.add_cog(RacingEvent(bot))
