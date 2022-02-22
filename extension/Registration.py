import asyncio

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.players import players, players_exists, players_register


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='open_bank')
    async def register_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/bank/bank.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='Create Bank Account', emoji='💷',
                           custom_id='open_book_bank'),
                    Button(style=ButtonStyle.blue, label='Check Bank Account', emoji='💷', custom_id='already_exists')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        bank_btn = interaction.component.custom_id

        if bank_btn == 'open_book_bank':
            player_check = players_exists(member.id)
            if player_check == 0:
                await interaction.respond(content='📝 กรุณาระบุ Steam ID ของคุณเพื่อลงเปิดบัญชีธนาคารและลงทะเบียน')
                while True:
                    try:
                        msg = await self.bot.wait_for('message',check=lambda m: m.author == interaction.author and m.channel == interaction.channel, timeout=10 )
                        a_string = str(msg.content)
                        length = len(a_string)
                        if msg.content.isdigit() and length == 17:
                            discord_id = str(member.id)
                            convert = discord_id[:5]
                            bank_id = str(convert)
                            players_register(member.name, member.id, msg.content, bank_id)
                            await interaction.channel.send(f'🎉 คุณได้เปิดบัญชีหมายเลข {bank_id} และลงทะเบียนสำเร็จแล้ว', delete_after=3)
                            await asyncio.sleep(3.5)
                            await msg.delete()
                            return
                        else:
                            await interaction.channel.send('รูปแบบ steam id ของคุณไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง', delete_after=5)
                            await asyncio.sleep(5.3)    
                            await msg.delete()
                    except asyncio.TimeoutError:
                        await interaction.channel.send('คุณใช้เวลาในการลงทะเบียนนานกว่าระบบกำหนด กรุณาลงทะเบียนใหม่อีกครั้ง',delete_after=3)
                        return
            if player_check == 1:
                player = players(member.id)
                await interaction.respond(content=f'คุณได้ลงทะเบียนไว้แล้ว หมายเลขบัญชีธนาคารของคุณคือ {player[9]}')
                return
                        

        if bank_btn == 'already_exists':
            player_check = players_exists(member.id)
            if player_check == 1:
                player = players(member.id)
                await interaction.respond(
                    content=f'Bank Statement\n-------------------------------------------------------------'
                    f'\nDiscord Name : {player[1]} \nBank ID : {player[9]} \nCoins : {player[10]}\n'
                    f'-------------------------------------------------------------\n'
                    f'power by {self.bot.user.name}'
                )
                return
            if player_check == 0:
                await interaction.respond(content='⚠ Not found your bank account !!!')


def setup(bot):
    bot.add_cog(Registration(bot))
