import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle
from players.players_db import update_steam_id, steam_check, exclusive_count, exclusive_update


class ServerInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server_info')
    @commands.has_permissions(manage_roles=True)
    async def server_info_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/info.png'),
        )
        await ctx.send(
            '**ChangThai℠ Really Survival** เซิร์ฟเวอร์ที่เน้นให้ผู้เล่น\n'
            'ได้เข้าถึงความเป็นเกมส์เอาชีวิตรอดอย่างแท้จริงจากระบบ\n'
            'Ai ของเกมส์ เน้นให้ผู้เล่นต่อสู้กับระบบ Ai และกลุ่มผู้เล่น เพื่อ\n'
            'แย่งชิงฐานที่มั่น ทรัพยากร และสิ่งอำนวยความสะดวกต่าง ๆ'
        )
        await ctx.send(file=discord.File('./img/info/setting.png'))
        await ctx.send(
            '- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 39 อัตราดรอป 3 เท่า\n'
            '- ปิดการแสดงแผนที่ จำกัดตี้เพียง 2 คนที่ค่า int Lvl5  \n'
            '- ยานพาหนะดรอปตามจำนวนสี ที่เหลือ trade เอากับ NPC\n'
            '- มีระบบ Guild มีภารกิจ เพิ่มช่องทางในการหาเงินให้ผู้เล่น\n'
            '- เน้นการสร้างสังคม ไม่ห้ามการรวมกลุ่ม หรือสร้างพันธมิตร\n'
            '- เพิ่มความเสียหายสำหรับช๊อตไฟฟ้า เป็น 50% \n'
            '- เลือกเกิด Sec: **200FP**, Ran: **100FP**, Shel: **100FP** \n'
            '- ซอมบี้ดาเมจ 3 เท่า 300 ตัวทั่วทั้งเกาะ ปล่อยหุ่นยนต์ \n'
            '- 1 วันของเกมส์เท่ากับ 4 ชั่วโมง 8 นาที ของเวลาจริง',
        )
        await ctx.send(file=discord.File('./img/info/caution.png'))
        await ctx.send(
            '- ห้ามผู้เล่นใช้ประโยชน์จากบัคในการสร้างสิ่งปลูกสร้าง\n'
            '- เรดบ้านได้ ตลอด 24 ชั่วโมง\n'
            '- ผู้เล่นสามารถรวมกลุ่มกันได้ ไม่จำกัด\n'
            '- ครอบครองยานพาหนะได้ไม่จำกัด \n'
            '- สร้างฐานได้ทุกที่ จำกัด 1 ธงต่อ 1 ตี้เท่านั้น \n'
            '- กับดักทุกชนิดห้ามวางนอกเขตธง (ฝ่าฝืนมีบทลงโทษ) \n'
            '- การช่วยเหลือ จะขึ้นอยู่กับแอดมินสะดวกหรือไม่ \n'
            '- การโกงการก่อกวน แบนออกทันทีหากพบว่าผิดจริง\n '
            '- การตัดสินใจของแอดมินและทีมงานถือเป็นที่สิ้นสุด'
        )
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        message = None
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
                return

            elif steamd_id is None:
                message = 'ไม่พบข้อมูล steam id ของคุณในระบบ กรุณาลงทะเบียน steam id ให้เรียบร้อย'
                await interaction.respond(content=message)
                return

        if btn == 'new_player':
            steam_id = steam_check(member.id)
            if steam_id is not None:
                await interaction.respond(content=f'{steam_id}')
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
                                update_steam_id(member.id, msg.content)
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
                            await interaction.channel.send('oh no.', delete_after=3)
                            await msg.delete()
                    except asyncio.TimeoutError:
                        await interaction.send(f'{member.mention} : 📢 คุณใช้เวลาในการลงทะเบียนนานเกินไป '
                                               f'กรุณาลงทะเบียนใหม่อีกครั้ง')

        if btn == 'get_gift':
            await interaction.respond(content=btn)

    @commands.command(name='reg_id')
    async def reg_id_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/server_register.png')
        )
        await ctx.send(
            'สำหรับผู้เล่นที่ต้องการเข้าร่วม Discord community เพื่อ \n'
            'ปรับสิทธิ์ในการใช้งาน Discord และเข้าถึงห้องต่าง ๆ โดย \n'
            'ให้ผู้เล่นกดที่ปุ่มด้านล่างและดำเนินการตามระบบต่อไป.',
            components=[
                Button(style=ButtonStyle.gray, emoji='📝', label='ลงทะเบียนผู้เล่น', custom_id='new_player')
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
            file=discord.File('./img/gift.png'),
            components=[
                Button(style=ButtonStyle.gray, label='GET FREE GIFT', emoji='🎁', custom_id='get_gift')
            ]
        )


def setup(bot):
    bot.add_cog(ServerInformation(bot))
