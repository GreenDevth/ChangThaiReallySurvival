import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Member_db import *


class ServerInformation(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(name='server_register')
    @commands.has_permissions(manage_roles=True)
    async def server_register(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/info.png'),
        )
        await ctx.send(
            'สัมผัสประสบการณ์สุดกดดัน แบบ Exclusive Members ไป\n'
            'พร้อมกับ **Really Survival** *Hardcore Version* เซิร์ฟเวอร์ที่\n'
            'อัดแน้นไปด้วยความเป็นเกมส์เอาชีวิตรอดแนว RPG 100%\n',
            file=discord.File('./img/register_new.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, emoji='📝', label='REGISTER NEW PLAYER', custom_id='new_player'),
                    Button(style=ButtonStyle.gray, emoji='🔐', label='ACTIVATE MEMBER', custom_id='activate_player')
                ]
            ]
        )
        await ctx.message.delete()

    @server_register.error
    async def server_register_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('ok', mention_author=False)


class RegisterMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id

        if btn == 'new_player':
            steam_id = steam_check(member.id)
            if steam_id is not None:
                await interaction.respond(
                    content=f'คุณได้ลงทะเบียนไว้เรียบร้อยแล้ว สตรีมไอดีของคุณคือ **{steam_id}** ✔')
            else:
                await interaction.send(f'{member.mention} : 📝 โปรดระบุ SteamID ของคุณเพื่อดำเนินการลงทะเบียน')
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
                            if length != 17:
                                print(length != 17)
                                await interaction.channel.send(
                                    f'{member.mention} : 📢 รูปแบบสตรีมไอดีของคุณไม่ถูกต้องกรุณาลองใหม่อีกครั้ง',
                                    delete_after=3)
                                await msg.delete()
                            else:
                                activatecode = generate_code(6)
                                update_steam_id(member.id, msg.content, activatecode)
                                await interaction.channel.send(
                                    f"🎉 ยินดีต้อนรับ {member.mention} ระบบกำลังดำเนินการจัดส่งรหัสปลดล็อคให้แก่คุณ",
                                    delete_after=5)
                                embed = discord.Embed(
                                    title="รหัสปลดล๊อคสำหรับสมัคร Exclusive Members",
                                    colour=discord.Colour.green()
                                )
                                embed.set_image(
                                    url="https://cdn.discordapp.com/attachments/894251225237848134/961097333876097034/unknown.png")
                                embed.add_field(name="ACTIVATE CODE", value=f"```\n{activatecode}\n```")
                                await discord.DMChannel.send(
                                    member,
                                    embed=embed
                                )
                                await msg.delete()
                                return
                        else:
                            await interaction.channel.send('รูปแบบสตรีมไอดีของคุณไม่ถูกต้อง', delete_after=3)
                            await msg.delete()
                    except asyncio.TimeoutError:
                        await interaction.send(f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป '
                                               f'กรุณาลงทะเบียนใหม่อีกครั้ง', delete_after=5)

        if btn == 'activate_player':
            steamd_id = member_check(member.id)
            if steamd_id is not None:
                check = verify_check(member.id)
                if check != 0:
                    await interaction.respond(
                        file=discord.File('./img/verify.png')
                    )
                elif check == 0:
                    await interaction.respond(
                        content='กรุณากรอกรหัสที่ได้จากเซิร์ฟเวอร์'
                    )

                    msg = await self.bot.wait_for(
                        'message',
                        check=lambda r: r.author == interaction.author and r.channel == interaction.channel)
                    check = activate_code_check(member.id)
                    if msg.content == check:
                        exclusive_channel = self.bot.get_channel(953622566105387048)
                        result = activate_code(check)
                        await exclusive_channel.send(
                            f"📃 **Exclusive Member {member.mention}**\n"
                            "```=====================================\n"
                            f"Discord name : {member.display_name}\n"
                            f"Discord id : {member.id}\n"
                            f"Steam id : {steamd_id}\n"
                            "Register status : ลงทะเบียนเรียบร้อย ✅\n"
                            "=====================================\n```"
                        )
                        await interaction.channel.send(f"{member.mention}\n{result}", delete_after=5)
                        verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                        role = discord.utils.get(interaction.guild.roles, name='joiner')
                        await member.add_roles(verify)
                        await member.remove_roles(role)
                        await discord.DMChannel.send(member, result)
                        await msg.delete()
                    else:
                        await interaction.channel.send('รหัสปลดล๊อคไม่ถูกต้อง กรุณาดำเนินการใหม่อีกครั้ง',
                                                       delete_after=5)
                        await msg.delete()

            else:
                await interaction.respond(
                    content='ไม่พบข้อมูล Steam id ของคุณในระบบ'
                )
