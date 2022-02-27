import discord
from discord.ext import commands
from discord_components import ButtonStyle, Button

class VoteSystemComands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_button_click(self, interation):
        racing = interation.component.custom_id
        count = 0
        if racing == 'tractor':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR {count + 1}', emoji='🚘', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'PICKUP {count}', emoji='🚘', custom_id='pickup_hell'),
                        Button(style=ButtonStyle.red, label=f'BIKE {count}', emoji='🚘', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'BYCICLE {count}', emoji='🚘', custom_id='bycicle')
                    ]
                ]
            )
        elif racing == 'pickup_hell':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR {count}', emoji='🚘', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'PICKUP {count + 1}', emoji='🚘', custom_id='pickup_hell'),
                        Button(style=ButtonStyle.red, label=f'BIKE {count}', emoji='🚘', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'BYCICLE {count}', emoji='🚘', custom_id='bycicle')
                    ]
                ]
            )
        elif racing == 'bike_hell':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR {count}', emoji='🚘', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'PICKUP {count}', emoji='🚘', custom_id='pickup_hell'),
                        Button(style=ButtonStyle.red, label=f'BIKE {count + 1}', emoji='🚘', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'BYCICLE {count}', emoji='🚘', custom_id='bycicle')
                    ]
                ]
            )
        elif racing == 'bycicle':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR {count}', emoji='🚘', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'PICKUP {count}', emoji='🚘', custom_id='pickup_hell'),
                        Button(style=ButtonStyle.red, label=f'BIKE {count}', emoji='🚘', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'BYCICLE {count + 1}', emoji='🚘', custom_id='bycicle')
                    ]
                ]
            )


    @commands.command(name='racing')
    async def racing_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/tractor.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='TRACTOR : 0', emoji='🚘', custom_id='tractor'),
                    Button(style=ButtonStyle.gray, label='PICKUP : 0', emoji='🚘', custom_id='pickup_hell'),
                    Button(style=ButtonStyle.red, label='BIKE : 0', emoji='🚘', custom_id='bike_hell'),
                    Button(style=ButtonStyle.green, label='BYCICLE : 0', emoji='🚘', custom_id='bycicle')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(VoteSystemComands(bot))