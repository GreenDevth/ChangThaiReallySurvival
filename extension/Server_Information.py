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
            '**SCUM** คือเกมส์เอาชีวิตรอดออนไลน์แบบผู้เล่นหลายคน \n'
            'และเพื่อให้เข้าถึงความเป็นเกมส์เอาชีวิตรอดที่แท้จริง เราจึง \n'
            'ได้ปรับแต่งเซิร์ฟที่เน้นระบบ Ai ของเกมส์ทำงานเป็นหลัก \n'
            'เพื่อให้ผู้เล่นได้เข้าถึงความเป็นเกมส์เอาชีวิตรอด และสนุก \n'
            'ไปกับเกมส์ SCUM ที่แตกต่างไปจากเซิร์ฟทั่วไป .',
            file=discord.File('./img/info/setting.png')
        )

        await ctx.send(
            '- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 39\n'
            '- อัตราการดรอปของ 1 และ 1.5 เท่า สำหรับของวางกับพื้น\n'
            '- ไม่มีกฎ ผู้เล่นสามารถทำอะไรได้เท่าที่เซิร์ฟเวอร์ได้ตั้งค่าไว้\n'
            '- ยานพาหนะไม่มีดรอป ทำภารกิจเพื่อรับรถหรือซื้อเท่านั้น \n'
            '- มีระบบธนาคารสำหรับเก็บสะสม SCUM Money \n'
            '- มีระบบ Guild สำหรับทำภารกิจเพื่อรับ รางวัลต่าง ๆ \n'
            '- ปิดการใช้งานกับดัก แผนที่ และข้อความระบบ\n '
            '- เพิ่มความเสียหายสำหรับช๊อตไฟฟ้า เป็น 50% \n '
            '- การเลือกเกิด Sector: ปิด , Random: 100FP, Shelter: 100FP \n '
            '- อัตราเฉลี่ยซอมบี้ต่อคน อยู่ที่ 50 ตัว ต่อพื้นที่ \n '
            '- 1 วันของเกมส์เท่ากับ 4 ชั่วโมง 8 นาที',
            file=discord.File('./img/info/rule.png')
        )
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


def setup(bot):
    bot.add_cog(ServerInformation(bot))
