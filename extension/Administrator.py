import discord
from discord.ext.commands import Cog


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
    #
    # @Cog.listener()
    # async def on_message(self, message):
    #     if message.content.startswith('clear'):
    #         if message.author.guild_permissions.administrator:
    #             await message.channel.purge()
    #             await message.channel.send('All message has been deleted.', mention_author=False, delete_after=5)
    #             return
    #         else:
    #             await message.channel.send('⚠ Only in Admin command!.', mention_author=False, delete_after=1)
    #             await asyncio.sleep(1)
    #             await message.delete()
    #
    # # @Cog.listener()
    # # async def on_command_error(self, ctx, error):
    # #     if isinstance(error, commands.CommandNotFound):
    # #         await ctx.reply('⚠ Your command not available or not found.', mention_author=False)
    #
    # @commands.command(name='unload')
    # async def unload_command(self, ctx, ext):
    #     self.bot.unload_extension(f'extension.{ext}')
    #     await ctx.reply('unload {} successfully.'.format(ext))
    #
    # @commands.command(name='load')
    # async def load_command(self, ctx, ext):
    #     self.bot.load_extension(f'extension.{ext}')
    #     await ctx.reply('load {} successfully.'.format(ext))
    #
    # @commands.Cog.listener()
    # async def on_button_click(self, interaction):
    #     btn = interaction.component.custom_id
    #     ext = "zombie_event"
    #     if btn == 'disable_ghost':
    #         self.bot.unload_extension(f'extension.{ext}')
    #         await interaction.respond(content=f'{ext} has been unload.')
    #     if btn == 'enable_ghost':
    #         self.bot.load_extension(f'extension.{ext}')
    #         await interaction.respond(content=f'{ext} has been load.')
    #
    # @commands.command(name='event_controller')
    # async def event_controller_command(self, ctx):
    #     await ctx.send(
    #         file=discord.File('./img/controller/controller.png'),
    #         components=[
    #             [
    #                 Button(style=ButtonStyle.red, label='Disable Event Zombie', emoji='👻', custom_id='disable_ghost'),
    #                 Button(style=ButtonStyle.green, label='Enable Event Zombie', emoji='👻', custom_id='enable_ghost')
    #             ]
    #         ]
    #     )
    #
    # @commands.command(name='check_players')
    # async def check_players_command(self, ctx, arg):
    #     player = players(arg)
    #     await ctx.reply('{}'.format(player))
    #
    # @commands.Cog.listener()
    # async def on_button_click(self, interaction):
    #     member = interaction.author
    #     btn = interaction.component.custom_id
    #
    #     if btn == 'free_money':
    #         check = players_exists(member.id)
    #         if check == 1:
    #             await interaction.respond(content="คุณได้รับเหรียญเนื่องในโอกาสพิเศษไปแล้ว")
    #         else:
    #             player = players(member.id)
    #             member_name = str(player[1])
    #             member_discord = str(player[2])
    #             member_steam = str(player[3])
    #             member_bank = int(player[4])
    #             member_coins = str(player[5])
    #             member_level = int(player[6])
    #             member_exp = str(player[8])
    #             await interaction.respond(content=f'{check}')
    #             transfer_player(member_name, member_discord, member_steam, member_level, member_exp, member_bank,
    #                             member_coins)
    #             print('New players has been transfer to SQLite...')
    #
    # # member = ctx.author
    # # player = players(member.id)
    # # name = player[1]
    # # discord_id = player[2]
    # # steam_id = player[3]
    # # bank_id = player[4]
    # # coins = player[5]
    # # level = player[6]
    # # exp = player[8]
    # # if member.id == discord_id:
    # #     await ctx.reply('ขออภัยคุณได้รับ รางวัลพิเศษไปแล้ว')
    # # else:
    # #     await ctx.reply('ขออภัยไม่พบข้อมูลของคุณ')
    # # await ctx.send(
    # #     f'Name: {player[1]}\n'
    # #     f'Discord_id: {player[2]}\n'
    # #     f'Steam_id: {player[3]}\n'
    # #     f'Bank_id: {player[4]}\n'
    # #     f'Coins: {player[5]}\n'
    # #     f'Level: {player[6]}\n'
    # #     f'Exp: {player[8]}\n'
    # # )
    #
    # @commands.command(name='get_coins')
    # async def get_coins_command(self, ctx):
    #     await ctx.send(
    #         'Get Coins',
    #         components=[Button(style=ButtonStyle.green, label='Free coins', emoji='💵', custom_id='free_money')]
    #     )


def setup(bot):
    bot.add_cog(AdministratorCommand(bot))
