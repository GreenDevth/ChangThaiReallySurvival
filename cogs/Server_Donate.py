import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle


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

    @commands.command(name='donate')
    async def donate_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/info/donate.png')
        )
        await ctx.send(
            "การสนับสนุนเซิร์ฟเป็นเพียงการช่วยเหลือค่าใช้จ่ายในการเช่าเซิร์ฟและบอท\n"
            "ผู้สนับสนุนจะไม่ได้อภิสิทธิ์ใดๆ นอกเหนื่อจากผู้เล่นคนอื่นๆ เว้นแต่จะได้รับ\n"
            "การช่วยเหลือตามความจำเป็น และสิทธิ์ในการเข้าใช้งานเซิร์ฟกรณีเซิร์ฟเต็ม\n",
            components=[
                Button(style=ButtonStyle.blue, label='สนับสนุนเซิร์ฟ', emoji='💳', custom_id='donate')
            ]
        )


def setup(bot):
    bot.add_cog(ServerDonation(bot))
