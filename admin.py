import asyncio

import discord
from discord.ext import commands
from database.Member_db import *


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f'Logged in as {self.bot.user.name}')
    #     await self.bot.change_presence(
    #         status=discord.Status.online,
    #         activity=discord.Activity(type=discord.ActivityType.playing, name='SCUM')
    #     )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('clear'):
            if message.author.guild_permissions.administrator:
                await message.channel.purge()
                await message.channel.send('**All message has been deleted.**', mention_author=False, delete_after=2)
                return
            else:
                await message.channel.send('⚠ Error, You can not used this commands.', mention_author=False,
                                           delete_after=1)
                await asyncio.sleep(1)
                await message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply('⚠ Error, {}'.format(error.args[0]), mention_author=False)
        await ctx.message.delete()

    @commands.command(name='verify')
    @commands.has_permissions(manage_roles=True)
    async def verify_command(self, ctx, member: discord.Member):
        result = update_to_exclusive(member.id)
        await ctx.reply(f'Send Message to {member.display_name} {result}', mention_author=False)
        await discord.DMChannel.send(member,
                                     f"สวัสดีครับคุณ {member.display_name} ระบบได้ ทำการปรับสิทธิ์ Exclusive Members ให้คุณเรียบร้อยแล้ว...")

    @verify_command.error
    async def verify_comman_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Only on Admin commands', mention_author=False)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument {}'.format(error.param), mention_author=False)


def setup(bot):
    bot.add_cog(Administrator(bot))
