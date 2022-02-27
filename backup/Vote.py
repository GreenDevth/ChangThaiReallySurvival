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
                        Button(style=ButtonStyle.blue, label=f'TRACTOR : {count + 1}', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'BYCICLE : {count}', custom_id='bycicle'),
                        Button(style=ButtonStyle.red, label=f'BIKE : {count}', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'SUV : {count}', custom_id='suv')
                    ]
                ]
            )
        elif racing == 'bycicle':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR : {count}', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'BYCICLE : {count + 1}', custom_id='bycicle'),
                        Button(style=ButtonStyle.red, label=f'BIKE : {count}', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'SUV : {count}', custom_id='suv')
                    ]
                ]
            )
        elif racing == 'bike_hell':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR : {count}', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'BYCICLE : {count}', custom_id='bycicle'),
                        Button(style=ButtonStyle.red, label=f'BIKE : {count + 1}', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'SUV : {count}', custom_id='suv')
                    ]
                ]
            )
        elif racing == 'suv':
            await interation.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.blue, label=f'TRACTOR : {count}', custom_id='tractor'),
                        Button(style=ButtonStyle.gray, label=f'BYCICLE : {count}', custom_id='bycicle'),
                        Button(style=ButtonStyle.red, label=f'BIKE : {count}', custom_id='bike_hell'),
                        Button(style=ButtonStyle.green, label=f'SUV : {count + 1}', custom_id='suv')
                    ]
                ]
            )


    @commands.command(name='racing')
    async def racing_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/tractor.jpg'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='TRACTOR : 0', custom_id='tractor'),
                    Button(style=ButtonStyle.gray, label='BYCICLE : 0', custom_id='bycicle'),
                    Button(style=ButtonStyle.red, label='BIKE : 0', custom_id='bike_hell'),
                    Button(style=ButtonStyle.green, label='SUV : 0', custom_id='SUV')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(VoteSystemComands(bot))