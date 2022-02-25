import asyncio
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from players.players_db import players_exists, update_steam_id


class ButtonEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        server_btn = interaction.component.costum_id

        if server_btn == 'new_players':
            check = players_exists(member.id)
            if check == 1:
                await interaction.respond(content='📝 กรุณาพิมพ์ steam id ของคุณที่นี่ เพื่อลงทะเบียน'
                                                  '\nPlease enter your steam id to register. ')
                while True:
                    try:
                        msg = await self.bot.wait_for(
                            'message',
                            check=lambda r: r.author == interaction.author and r.channel == interaction.channel,
                            timeout=300
                        )
                        if msg.content.isdigit():
                            a_string = str(msg.content)
                            length = len(a_string)

                            discord_name = str(member.name)
                            discord_id = str(member.id)
                            convert = discord_id[:5]
                            bank_id = str(convert)

                            if length == 17:
                                update_steam_id(discord_id, msg.content)
                                await discord.DMChannel.send(
                                    member,
                                    "🎉 ยินดีต้อนรับอย่างเป็นทางการสู่สังคม ChangThai℠ Really survival "
                                )
                                verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                                role = discord.utils.get(interaction.guild.roles, name='joiner')
                                await member.add_roles(verify)
                                await member.remove_roles(role)
                                await msg.delete()
                                return

                        else:
                            await interaction.channel.send(
                                f'{member.mention} : 📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                delete_after=5)
                            await msg.delete()

                    except asyncio.TimeoutError:
                        await interaction.send(
                            f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป กรุณาลงทะเบียนใหม่อีกครั้ง'
                        )



def setup(bot):
    bot.add_cog(ButtonEvent(bot))
