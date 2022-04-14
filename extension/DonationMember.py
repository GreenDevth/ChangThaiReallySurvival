import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Donate_db import *

now = datetime.now()
create_at = now.strftime("%H:%M:%S")


class ServerDonation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ Create Donation Commands """

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        donate_btn = interaction.component.custom_id
        donate_room = get_donate_room(member.id)
        if donate_btn == 'donate':
            discord_member = players_check(member.id)
            if discord_member == 1:
                player_id = get_players_id(member.id)
                check = donate_players(member.id)
                if check == 0:
                    channel_name = interaction.guild.get_channel(donate_room)
                    if channel_name is None:
                        await interaction.respond(content="โปรดรอสักครู่ระบบกำลังสร้างห้องให้กับคุณ")
                        categorys = discord.utils.get(interaction.guild.categories, name="DONATE SERVER")
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                        connect=False),
                            member: discord.PermissionOverwrite(read_messages=True)
                        }
                        new_donate_channel = f'ห้องสนับสนุน-{player_id}'
                        await categorys.edit(overwrites=overwrites)
                        await interaction.guild.create_text_channel(new_donate_channel, category=categorys)
                        channel = discord.utils.get(interaction.guild.channels, name=str(new_donate_channel))
                        channel_send = interaction.guild.get_channel(channel.id)
                        create_new_donate_member(member.id, member.name, channel.id, create_at)
                        embed = discord.Embed(
                            title="ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ",
                            description="ชื่อบัญชี นายธีรพงษ์ บัวงาม",
                            color=discord.Colour.green(),
                        )
                        embed.add_field(name="บัญชีธนาคารกสิกรไทย", value="035-8-08192-4")
                        embed.add_field(name="หมายเลข Promtpay", value="0951745515")
                        await channel_send.send(
                            file=discord.File('./img/donate_banner.png')
                        )
                        await channel_send.send(
                            "============================\n"
                            "**ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ**"
                            "============================\n"
                            "\nชื่อบัญชี นายธีรพงษ์ บัวงาม ธนาคารกสิกรไทย"
                            "\nเลขที่ **035-8-08192-4**"
                            "\nหมายเลขพร้อมเพย์"
                            "\n**0951745515**"
                        )
                        await channel_send.send(
                            file=discord.File('./img/upload_img.png'),
                            components=[
                                Button(style=ButtonStyle.blue, label='อัพโหลดสลิป', emoji='📸', custom_id='donate_img')]
                        )
                        await interaction.channel.send(f'ไปยังห้องของคุณ <#{channel.id}>', delete_after=5)
                    if channel_name is not None:
                        await interaction.respond(content=f'ไปยังห้องของคุณ <#{donate_room}')
                elif check == 1:
                    channel_name = interaction.guild.get_channel(donate_room)
                    if channel_name is None:
                        await interaction.respond(content="โปรดรอสักครู่ระบบกำลังสร้างห้องให้กับคุณ")
                        categorys = discord.utils.get(interaction.guild.categories, name="DONATE SERVER")
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                        connect=False),
                            member: discord.PermissionOverwrite(read_messages=True)
                        }
                        new_donate_channel = f'ห้องสนับสนุน-{player_id}'
                        await categorys.edit(overwrites=overwrites)
                        await interaction.guild.create_text_channel(new_donate_channel, category=categorys)
                        channel = discord.utils.get(interaction.guild.channels, name=str(new_donate_channel))
                        channel_send = interaction.guild.get_channel(channel.id)
                        update_date_channel(member.id, channel.id)
                        embed = discord.Embed(
                            title="ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ",
                            description="ชื่อบัญชี นายธีรพงษ์ บัวงาม",
                            color=discord.Colour.green(),
                        )
                        embed.add_field(name="บัญชีธนาคารกสิกรไทย", value="035-8-08192-4")
                        embed.add_field(name="หมายเลข Promtpay", value="0951745515")
                        await channel_send.send(
                            file=discord.File('./img/donate_banner.png')
                        )
                        await channel_send.send(
                            "============================\n"
                            "**ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ**"
                            "============================\n"
                            "\nชื่อบัญชี นายธีรพงษ์ บัวงาม ธนาคารกสิกรไทย"
                            "\nเลขที่ **035-8-08192-4**"
                            "\nหมายเลขพร้อมเพย์"
                            "\n**0951745515**"
                        )
                        await channel_send.send(
                            file=discord.File('./img/upload_img.png'),
                            components=[
                                Button(style=ButtonStyle.blue, label='อัพโหลดสลิป', emoji='📸', custom_id='donate_img')]
                        )
                        await interaction.channel.send(f'ไปยังห้องของคุณ <#{channel.id}>', delete_after=5)
                    if channel_name is not None:
                        channel_send = interaction.guild.get_channel(int(donate_room))
                        await interaction.respond(content=f'ไปยังห้องของคุณ <#{donate_room}>')
                        await channel_send.send(
                            file=discord.File('./img/donate_banner.png')
                        )
                        await channel_send.send(
                            "=========================================\n"
                            "**==== ช่องทางสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟ ====**\n"
                            "=========================================\n"
                            "\nชื่อบัญชี นายธีรพงษ์ บัวงาม ธนาคารกสิกรไทย"
                            "\nเลขที่ **035-8-08192-4**"
                            "\nหมายเลขพร้อมเพย์ **0951745515**"
                        )
                        await channel_send.send(
                            file=discord.File('./img/upload_img.png'),
                            components=[
                                Button(style=ButtonStyle.blue, label='อัพโหลดสลิป', emoji='📸', custom_id='donate_img')]
                        )
            elif discord_member == 0:
                await interaction.respond(content="ไม่พบข้อมูลการลงทะเบียนของคุณในระบบ")

        if donate_btn == 'donate_img':
            donate = self.bot.get_channel(int(donate_room))
            await interaction.respond(content='กรุณาอัพโหลดสลิปของคุณ')

            def check(res):
                attachments = res.attachments
                if len(attachments) == 0:
                    return False
                attachment = attachments[0]
                file_type = attachment.filename.endswith(('.jpg', '.png', 'jpeg'))
                return res.author == interaction.author and res.channel == interaction.channel and file_type

            msg = await self.bot.wait_for('message', check=check)
            if msg is not None:
                await interaction.channel.send(f'{member.mention}\nขอบคุณสำหรับการสนับสนุนเซิร์ฟในครั้งนี้', delete_after=10)
            image = msg.attachments[0]
            embed = discord.Embed(
                title=f'ผู้สนับสนุนเซิร์ฟ {member.name}',
                description='ขอขอบคุณเป็นอย่างยิ่งสำหรับการสนับสนุนค่าใช้จ่ายเซิร์ฟในครั้งนี้ ',
                timestamp=datetime.utcnow(),
                color=discord.Colour.green()
            )
            embed.set_author(name=f'{member.name}', icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(url=image)
            embed.add_field(name='ผู้สนับสนุนเซิร์ฟ', value=member.mention, inline=False)
            owner = interaction.guild.get_member(499914273049542677)
            await discord.DMChannel.send(owner, embed=embed)
            send = await donate.send(embed=embed)
            await send.add_reaction("😍")

    @commands.command(name='donate')
    async def donate_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/donate_t.png')
        )
        await ctx.send(
            "การสนับสนุนเซิร์ฟเป็นเพียงการช่วยเหลือค่าใช้จ่ายของเซิร์ฟ\n"
            "ผู้สนับสนุนจะไม่ได้อภิสิทธิ์ใดๆ นอกเหนื่อจากผู้เล่นคนอื่นๆ \n"
            "เว้นแต่จะได้รับการช่วยเหลือตามความจำเป็น และสิทธิ์ในการ\n"
            "เข้าใช้งานเซิร์ฟกรณีเซิร์ฟเต็ม\n"
        )
        await ctx.send(
            file=discord.File('./img/donate.png'),
            components=[
                Button(style=ButtonStyle.red, label='สนับสนุนเซิร์ฟ', emoji='💳', custom_id='donate')
            ]
        )
        await ctx.message.delete()


