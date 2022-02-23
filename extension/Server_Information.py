import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle


class ServerInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server_info')
    async def server_info_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/info.png'),
        )
        await ctx.send(
            '**ChangThai℠ Really Survival** เซิร์ฟเวอร์ที่มีที่เน้นให้ผู้เล่น\n'
            'ได้เข้าถึงความเป็นเกมส์เอาชีวิตรอดอย่างแท้จริงจากระบบ Ai\n'
            'ของเกมส์ เน้นให้ผู้เล่นต่อสู้กับระบบ Ai ของเกมส์ ต่อสู้แย่งชิง\n'
            'ฐานที่มั่น ทรัพยากร และสิ่งอำนวยความสะดวกต่าง ๆ'
        )
        await ctx.send(file=discord.File('./img/info/setting_2.png'))
        await ctx.send(
            '- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 39 อัตราดรอป 1 เท่า\n'
            '- ปิดการแสดงแผนที่ กับดักและจำกัดตี้เพียง 1 คน \n'
            '- ยานพาหนะไม่มีดรอป ต้องหาเงิน trade เอา กับ NPC เท่านั้น\n'
            '- มีระบบ Guild มีภารกิจ เพิ่มช่องทางในการหาเงินให้ผู้เล่น\n'
            '- เน้นการสร้างสังคม ไม่ห้ามการรวมกลุ่ม หรือสร้างพันธมิตร\n'
            '- เพิ่มความเสียหายสำหรับช๊อตไฟฟ้า เป็น 50% \n'
            '- การเลือกเกิด Sector: ปิด , Random: 100FP, Shelter: 100FP \n'
            '- ซอมบี้ดาเมจ 1 เท่า 50 ตัว ต่อ คน ต่อ พื้นที่ \n'
            '- 1 วันของเกมส์เท่ากับ 4 ชั่วโมง 8 นาที ของเวลาจริง',
        )
        await ctx.send(file=discord.File('./img/info/caution.png'))
        await ctx.send(
            '- ห้ามผู้เล่นใช้ประโยชน์จากบัคในการสร้างสิ่งปลูกสร้าง\n'
            '- เรดบ้านได้ ตลอด 24 ชั่วโมง\n'
            '- ผู้เล่นสามารถรวมกลุ่มกันได้ ไม่จำกัด\n'
            '- ครอบครองยานพาหนะได้ไม่จำกัด \n'
            '- สร้างฐานได้ทุกที่ แต่จำกัด 1 ธงต่อ 1 ผู้เล่นเท่านั้น \n'
            '- การช่วยเหลือ จะขึ้นอยู่กับแอดมินสะดวกหรือไม่ \n'
            '- การโกงการก่อกวน แบนออกทันทีหากพบว่าผิดจริง\n '
            '- การตัดสินใจของแอดมินและทีมงานถือเป็นที่สิ้นสุด'
        )

        await ctx.message.delete()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(866926077246832680)
        welcome = guild.get_channel(914080006429360149)
        role = discord.utils.get(guild.roles, name="joiner")
        await member.add_roles(role)

        await welcome.send(f"{member.mention} : {member.name} ได้เข้าร่วมเซิร์ฟของเราแล้ว")
        await discord.DMChannel.send(
            member,
            "**⚔ ChangThai℠ Really survival**\n\n" +
            "\n- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 30 อัตราดรอป 1.0"
            "\n- ไอพีเซิร์ฟ : 143.244.33.48:7102 รหัสผ่าน 28702"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(866926077246832680)
        leave = guild.get_channel(937573869361979422)
        await leave.send(f"{member.mention} : {member.name} ได้ออกจากเซิร์ฟของเราแล้ว")



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

def setup(bot):
    bot.add_cog(ServerInformation(bot))
