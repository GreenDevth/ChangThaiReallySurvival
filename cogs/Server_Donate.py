import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle
from datetime import datetime

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

        if donate_btn == 'donate':
            await interaction.respond(content='ระบบกำลังส่งข้อมูลสำหรับการสนับสนุน'
                                              'ค่าใช้จ่ายเซิร์ฟไปยังข้อความส่วนตัวของคุณ')
            await discord.DMChannel.send(
                member,
                ":credit_card: **ช่องทางในการสนับสนุนเซิร์ฟเวอร์**\n"
                "ผ่านบัญชีธนาคาร กสิกรไทย **035-8-08192-4** นายธีรพงษ์ บัวงามหมายเลข\n"
                "PromptPay : **0951745515**"
            )
        if donate_btn == 'donate_img':
            donate = self.bot.get_channel(946805199010426881)
            await interaction.respond(content='กรุณาอัพโหลดสลิปของคุณ')

            def check(message):
                attachments = message.attachments
                if len(attachments) == 0:
                    return False
                attachment = attachments[0]
                return attachment.filename.endswith(('.jpg', '.png'))

            msg = await self.bot.wait_for('message', check=check)
            if msg is not None:
                await interaction.channel.send('ขอบคุณสำหรับการสนับสนุนเซิร์ฟในครั้งนี้', delete_after=5)
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
            send = await donate.send(embed=embed)
            await send.add_reaction("😍")
            await msg.delete()

    @commands.command(name='donate')
    async def donate_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/donate.png')
        )
        await ctx.send(
            "การสนับสนุนเซิร์ฟเป็นเพียงการช่วยเหลือค่าใช้จ่ายของเซิร์ฟ\n"
            "ผู้สนับสนุนจะไม่ได้อภิสิทธิ์ใดๆ นอกเหนื่อจากผู้เล่นคนอื่นๆ \n"
            "เว้นแต่จะได้รับการช่วยเหลือตามความจำเป็น และสิทธิ์ในการ\n"
            "เข้าใช้งานเซิร์ฟกรณีเซิร์ฟเต็ม\n",
            components=[
                [
                    Button(style=ButtonStyle.red, label='สนับสนุนเซิร์ฟ', emoji='💳', custom_id='donate'),
                    Button(style=ButtonStyle.gray, label='อัพโหลดสลิป', emoji='📷', custom_id='donate_img')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(ServerDonation(bot))
