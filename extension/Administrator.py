import asyncio

from discord_components import Button, ButtonStyle
import discord
from discord.ext.commands import Cog
from discord.ext import commands


class AdministratorCommand(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count - 1
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name='ผู้ใช้งาน {} คน'.format(members))
        )

    @Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('clear'):
            if message.author.guild_permissions.administrator:
                await message.channel.purge()
                await message.channel.send('All message has been deleted.', mention_author=False, delete_after=5)
                return
            else:
                await message.channel.send('⚠ Only in Admin command!.', mention_author=False, delete_after=1)
                await asyncio.sleep(1)
                await message.delete()

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply('⚠ Your command not available or not found.', mention_author=False)

    @commands.command(name='unload')
    async def unload_command(self, ctx, ext):
        self.bot.unload_extension(f'extension.{ext}')
        await ctx.reply('unload {} successfully.'.format(ext))

    @commands.command(name='load')
    async def load_command(self, ctx, ext):
        self.bot.load_extension(f'extension.{ext}')
        await ctx.reply('load {} successfully.'.format(ext))

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        btn = interaction.component.custom_id
        ext = "zombie_event"
        if btn == 'disable_ghost':
            self.bot.unload_extension(f'extension.{ext}')
            await interaction.respond(content=f'{ext} has been unload.')
        if btn == 'enable_ghost':
            self.bot.load_extension(f'extension.{ext}')
            await interaction.respond(content=f'{ext} has been load.')

    @commands.command(name='event_controller')
    async def event_controller_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/controller/controller.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label='Disable Event Zombie', emoji='👻', custom_id='disable_ghost'),
                    Button(style=ButtonStyle.green, label='Enable Event Zombie', emoji='👻', custom_id='enable_ghost')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(AdministratorCommand(bot))
