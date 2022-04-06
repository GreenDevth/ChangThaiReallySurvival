import random

import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle
from players.players_db import *
from extension.Manage_Members import ManageMembers


def generate_code(length):
    string_code = 'reallysurvival'
    result = ''.join((random.choice(string_code)) for x in range(length))
    return result.upper()


class ServerInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server_info')
    @commands.has_permissions(manage_roles=True)
    async def server_info_command(self, ctx):
        await ctx.message.delete()
        await ctx.send(
            file=discord.File('./img/info/info.png'),
        )
        await ctx.send(
            'สัมผัสประสบการณ์สุดกดดัน แบบ Exclusive Members ไป\n'
            'กับ **ChangThai℠ Really Survival** เซิร์ฟเวอร์ที่อัดเน้นไปด้วย\nความเป็นเกมส์เอาชีวิตรอด 100%'
            '\n\nและหากคุณก็เป็นหนึ่งในผู้เล่นที่แสวงหาความยาก ความ\nสมจริง และความเป็น Survival Server อย่างแท้จริง\n**ChangThai℠ Really Survival** จะเป็นเซิร์ฟเวอร์ที่ตอบโจทย์\nความต้องการของคุณได้อย่างแน่นอน'
            '\n\nโปรดเตรียม Steam ID ไว้สำหรับสมัครใช้งานที่ห้อง\n <#918381749833171005>\n',
            components=[
                [
                    Button(style=ButtonStyle.gray, label='SERVER SETTING', emoji='⚙', custom_id='server_setting'),
                    Button(style=ButtonStyle.red, label='SERVER CAUTION', emoji='⚠', custom_id='server_caution')
                ]
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        if btn == 'exclusive_count':
            count = exclusive_count()
            await interaction.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.green, label='EXCLUSIVE REGISTER',
                               emoji='📝', custom_id='exclusive'),
                        Button(style=ButtonStyle.blue, label='EXCLUSIVE MEMBER : {}'.format(count),
                               emoji='📜', custom_id='exclusive_count')
                    ]
                ]
            )
        if btn == 'exclusive':
            steamd_id = steam_check(member.id)
            exclusive_channel = self.bot.get_channel(953622566105387048)
            if steamd_id is not None:
                exclusive_update(member.id)
                count = exclusive_count()
                await interaction.edit_origin(
                    components=[
                        [
                            Button(style=ButtonStyle.green, label='EXCLUSIVE REGISTER',
                                   emoji='📝', custom_id='exclusive'),
                            Button(style=ButtonStyle.blue, label='EXCLUSIVE MEMBER : {}'.format(count),
                                   emoji='📜', custom_id='exclusive_count')
                        ]
                    ]
                )
                message = 'คุณได้สมัครเข้าร่วม Exclusive Members ไว้เรียบร้อย'
                await discord.DMChannel.send(member, message)
                await exclusive_channel.send(
                    "📃 **Exclusive Member {}**\n"
                    "```=====================================\n"
                    "ผู้ลงทะเบียน : {}\n"
                    "ดิสคอร์ดไอดี : {}\n"
                    "สตรีมไอดี : {}\n"
                    "สถานะ : ลงทะเบียนเรียบร้อย ✅\n"
                    "=====================================\n```".format(member.display_name, member.display_name,
                                                                        member.id, steamd_id)
                )
                return

            elif steamd_id is None:
                message = 'ไม่พบข้อมูล steam id ของคุณในระบบ กรุณาลงทะเบียน steam id ให้เรียบร้อย'
                await interaction.respond(content=message)
                return

        if btn == 'new_player':
            steam_id = steam_check(member.id)
            if steam_id is not None:
                await interaction.respond(content=f'คุณได้ลงทะเบียนไว้เรียบร้อยแล้ว สตรีมไอดีของคุณคือ **{steam_id}**')
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
                                    "🎉 ยินดีต้อนรับอย่างเป็นทางการสู่สังคม ChangThai℠ Really survival ", delete_after=5)
                                await discord.DMChannel.send(
                                    member, f"รหัสปลดล๊อคของคุณคือ```cs\n'{activatecode}'\n```",
                                    file=discord.File('./img/activate_code.png')
                                )
                                verify = discord.utils.get(interaction.guild.roles, name='Verify Members')
                                role = discord.utils.get(interaction.guild.roles, name='joiner')
                                await member.add_roles(verify)
                                await member.remove_roles(role)
                                await msg.delete()
                                return
                        else:
                            await interaction.channel.send('oh no.', delete_after=3)
                            await msg.delete()
                    except asyncio.TimeoutError:
                        await interaction.send(f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป '
                                               f'กรุณาลงทะเบียนใหม่อีกครั้ง')

        if btn == 'get_gift':
            await interaction.respond(content=btn)

        if btn == 'server_setting':
            await interaction.respond(
                content='- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 39 อัตราดรอป 3 เท่า\n'
                        '- เปิดใช้งานเซิร์ฟแบบ Exclusive Members\n'
                        '- ปิดการแสดงแผนที่ จำกัดตี้เพียง 2 คนที่ค่า int Lvl5  \n'
                        '- ยานพาหนะดรอปตามจำนวนสี ที่เหลือ trade เอากับ NPC\n'
                        '- มีระบบ Guild มีภารกิจ เพิ่มช่องทางในการหาเงินให้ผู้เล่น\n'
                        '- เน้นการสร้างสังคม ไม่ห้ามการรวมกลุ่ม หรือสร้างพันธมิตร\n'
                        '- เพิ่มความเสียหายสำหรับช๊อตไฟฟ้า เป็น 50% \n'
                        '- เลือกเกิด Sec: **200FP**, Ran: **100FP**, Shel: **100FP** \n'
                        '- ซอมบี้ดาเมจ 3 เท่า 250 ตัวทั่วทั้งเกาะ ปล่อยหุ่นยนต์ \n'
                        '- 1 วันของเกมส์เท่ากับ 4 ชั่วโมง 8 นาที ของเวลาจริง',
            )
        if btn == 'server_caution':
            await interaction.respond(
                content='- ห้ามผู้เล่นใช้ประโยชน์จากบัคในการสร้างสิ่งปลูกสร้าง\n'
                        '- เรดบ้านได้ ตลอด 24 ชั่วโมง\n'
                        '- ผู้เล่นสามารถรวมกลุ่มกันได้ ไม่จำกัด\n'
                        '- ครอบครองยานพาหนะได้ไม่จำกัด \n'
                        '- สร้างฐานได้ทุกที่ จำกัด 1 ธงต่อ 1 ตี้เท่านั้น \n'
                        '- กับดักทุกชนิดห้ามวางนอกเขตธง (ฝ่าฝืนมีบทลงโทษ) \n'
                        '- การช่วยเหลือ จะขึ้นอยู่กับแอดมินสะดวกหรือไม่ \n'
                        '- การโกงการก่อกวน แบนออกทันทีหากพบว่าผิดจริง\n '
                        '- การตัดสินใจของแอดมินและทีมงานถือเป็นที่สิ้นสุด'
            )
        if btn == 'activate_player':
            steamd_id = steam_check(member.id)
            if steamd_id is not None:
                check = verify_check(member.id)
                if check != 0:
                    await interaction.respond(content="คุณได้ปลดล๊อคการใช้งาน Exclusive Member เรียบร้อยแล้ว")
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
                            f"ผู้ลงทะเบียน : {member.display_name}\n"
                            f"ดิสคอร์ดไอดี : {member.id}\n"
                            f"สตรีมไอดี : {steamd_id}\n"
                            "สถานะ : ลงทะเบียนเรียบร้อย ✅\n"
                            "=====================================\n```"
                        )
                        await interaction.channel.send(f"{member.mention}\n{result}", delete_after=5)
                        await discord.DMChannel.send(member, result)
                        await msg.delete()
                    else:
                        await interaction.channel.send('รหัสปลดล๊อคไม่ถูกต้อง กรุณาดำเนินการใหม่อีกครั้ง', delete_after=5)
                        await msg.delete()

            else:
                await interaction.respond(
                    content='ไม่พบข้อมูล Steam id ของคุณในระบบ'
                )

    @commands.command(name='reg_id')
    async def reg_id_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/register.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, emoji='📝', label='REGISTER NEW PLAYER', custom_id='new_player'),
                    Button(style=ButtonStyle.gray, emoji='🔐', label='ACTIVATE MEMBER', custom_id='activate_player')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='exclusive')
    async def exclusive_command(self, ctx):
        count = exclusive_count()
        await ctx.send(
            file=discord.File('./img/exclusive.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='EXCLUSIVE REGISTER',
                           emoji='📝', custom_id='exclusive'),
                    Button(style=ButtonStyle.blue, label='EXCLUSIVE MEMBER : {}'.format(count),
                           emoji='📜', custom_id='exclusive_count')
                ]
            ]
        )

    @commands.command(name='gift')
    async def gift_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/gift_l.png'),
            components=[
                Button(style=ButtonStyle.gray, label='GET YOUR GIFT', emoji='🎁', custom_id='get_gift')
            ]
        )


def setup(bot):
    bot.add_cog(ServerInformation(bot))
    bot.add_cog(ManageMembers(bot))
