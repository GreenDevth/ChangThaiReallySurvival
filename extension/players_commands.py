from discord.ext import commands
from discord_components import Button, ButtonStyle


class PlayerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Player command online')

    @commands.command(name='bank')
    async def bank_command(self, ctx):
        await ctx.reply('your bank balance is this', mention_author=False)

    @commands.command(name='selfbutton')
    async def selfbutton_command(self, ctx):
        await ctx.send(
            '💻 **ระบบแสดงข้อมูล**',
            components=[
                [
                    
                ]
            ]
        )
    
def setup(bot):
    bot.add_cog(PlayerCommand(bot))
