import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle


class SelfButtonCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='selfbutton')
    async def self_button_command(self, ctx):
        await ctx.send(
            '🖥 **Self button control.**',
            components=[
                [
                    Button(style=ButtonStyle.grey, label='Bank Statement', emoji='🏛'),
                    Button(style=ButtonStyle.grey, label='Server Status', emoji='🌏'),
                    Button(style=ButtonStyle.grey, label='Daily Pack', emoji='🍔')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(SelfButtonCommand(bot))
