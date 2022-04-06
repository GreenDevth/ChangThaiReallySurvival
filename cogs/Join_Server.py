import discord
from discord.ext import commands
import datetime
from players.players_db import new_players, remove_player


class WelcomeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(866926077246832680)
        welcome = guild.get_channel(914080006429360149)
        role = discord.utils.get(guild.roles, name='joiner')
        await member.add_roles(role)
        discord_id = str(member.id)
        convert = discord_id[:5]
        # bank_id = str(convert)
        name = str(member.name)
        x = datetime.datetime.now()
        join_date = x.strftime("%A %B %Y")

        new_players(name, int(member.id), convert, join_date)
        await welcome.send(f'{member.mention} : {member.name} ได้เข้าร่วมดิสคอร์สของเราแล้ว')
        img = "https://cdn.discordapp.com/attachments/894251225237848134/961091814692118538/hardcord_poster.png"
        embed = discord.Embed(
            title='ChangThai℠ Really Survival',
            description="กรุณาเตรียม สตรีมไอดีของคุณ ไว้สำหรับลงทะเบียนและรับรหัสปลดล็อคจากเซิร์ฟ"
        )
        embed.set_image(url=img)
        await discord.DMChannel.send(
            member,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(866926077246832680)
        leave = guild.get_channel(937573869361979422)
        remove_player(member.id)
        await leave.send(f"{member.mention} : {member.name} ได้ออกจากเซิร์ฟของเราแล้ว")


def setup(bot):
    bot.add_cog(WelcomeCommands(bot))
