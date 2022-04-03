import discord
from discord.ext import commands


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(
            title='Help',
            description='Use !help <command> for extended information on a command.',
            color=discord.Colour.orange(),
        )
        em.add_field(name='Transaction', value='bank, dmbank, status, daily', inline=False)
        em.add_field(name='server information', value='server_infor, reg_id, get_ip, server, selfserve', inline=False)
        await ctx.send(embed=em)

    @help.command(name='bank')
    async def bank(self, ctx):
        em = discord.Embed(
            title='Bank',
            description='แสดงข้อมูล Member Bank Statement',
            color=discord.Colour.orange()
        )
        em.add_field(name='**Syntax**', value='!bank')
        em.add_field(name='Permission', value='Verify Member ทุกคนใช้งานคำสั่งนี้ได้')
        await ctx.send(embed=em)

    @help.command(name='dmbank')
    async def dmbank(self, ctx):
        em = discord.Embed(
            title="Dmbank",
            description='แสดงข้อความ Bank Statement แบบส่วนตัว',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!dmbank')
        em.add_field(name='Permission', value='Verify Member ทุกคนใช้งานคำสั่งนี้ได้')
        await ctx.send(embed=em)

    @help.command(name='transfer')
    async def transfer(self, ctx):
        em = discord.Embed(
            title="Transfer Command",
            description='คำสั่งโอนเงินดิสคอร์ดให้กับผู้เล่นอื่น',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!transfer [bank_id] [amount]')
        em.add_field(name='Permission', value='Verify Member ทุกคนใช้งานคำสั่งนี้ได้')
        await ctx.send(embed=em)

    @help.command(name='status')
    async def status(self, ctx):
        em = discord.Embed(
            title="Status",
            description='แสดงข้อความข้อมูลของตัวเอง',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!status')
        em.add_field(name='Permission', value='Verify Member ทุกคนใช้งานคำสั่งนี้ได้')
        await ctx.send(embed=em)

    @help.command(name='daily')
    async def daily(self, ctx):
        em = discord.Embed(
            title="Daily",
            description='คำสั่งสำหรับเรียกใช้งาน Daily Pack ประจำวัน ',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!daily')
        em.add_field(name='Permission', value='Verify Member ทุกคนใช้งานคำสั่งนี้ได้')
        await ctx.send(embed=em)

    @help.command(name='check')
    async def check(self, ctx):
        em = discord.Embed(
            title="Check Player Status",
            description='แสดงข้อความรายละเอียด Register Member แบบย่อ',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!check [discord id]')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='reset_daily')
    async def reset_daily(self, ctx):
        em = discord.Embed(
            title="Reset Daily Pack",
            description='คำสั่งสำหรับรีเซ็ต Daily Pack ให้ผู้เล่นทุกคน',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!reset_daily')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='load_button')
    async def load_button(self, ctx):
        em = discord.Embed(
            title="Load Controller Button",
            description='แสดงปุ่มสำหรับจัดการ Extension[load, re-load, unload]',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!load_button')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='update')
    async def update(self, ctx):
        em = discord.Embed(
            title="Update Stock Item",
            description='คำสั่งสำหรับปรับจำนวนสต๊อกของไอเท็ม',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!update [item commands]] [amount]')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='item_lists')
    async def item_lists(self, ctx):
        em = discord.Embed(
            title="List all item",
            description='แสดงข้อความ list ของไอเท็มที่มีจำหน่ายทั้งหมด',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!item_lists')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='reg_id')
    async def reg_id(self, ctx):
        em = discord.Embed(
            title="List all item",
            description='แสดงข้อความโมดูลลงทะเบียนผู้เล่น',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!reg_id')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='gift')
    async def gift(self, ctx):
        em = discord.Embed(
            title="Module random gift",
            description='แสดงข้อความโมดูลปุ่มกดรับของรางวัล',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!gift')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='server_info')
    async def server_info(self, ctx):
        em = discord.Embed(
            title="Module Server information",
            description='แสดงโมดูลข้อมูลของเซิร์ฟเวอร์',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!server_info')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)

    @help.command(name='donate')
    async def donate(self, ctx):
        em = discord.Embed(
            title="Donate Module",
            description='แสดงโมดูลแสดงข้อมูลการสนับสนุนเซิร์ฟ',
            color=discord.Colour.orange()
        )
        em.add_field(name='Syntax', value='!donate')
        em.add_field(name='Permission', value='สำหรับแอดมินเท่านั้น')
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
