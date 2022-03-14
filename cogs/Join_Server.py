import discord
from discord.ext import commands
from players.players_db import players_exists, new_players, remove_player


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
        bank_id = str(convert)
        name = str(member.name)
        new_players(name, int(member.id), convert)
        await welcome.send(f'{member.mention} : {member.name} ได้เข้าร่วมดิสคอร์สของเราแล้ว')
        await discord.DMChannel.send(
            member,
            "**⚔ ChangThai℠ Really survival**\n\n" +
            "\n- เซิร์ฟสิงคโปร์ ปิงเริ่มต้นที่ 30 อัตราดรอป 3 ซอมบี้ 300 ดาเมจ 3 เท่า มีหุ่นยนต์"
            "\n- ปิดแผนที่ ตี้ สูงสุด 2 คนที่ค่า int Lvl5"
            "\n- ห้ามวางกับดักนอกเขตธง พบเห็นจะหักเงินและเฟรมฟ้อยทั้งหมดทันที พร้อมบทลงโทษอื่น ๆ"
            "\n- ไอพีเซิร์ฟ : 143.244.33.48:7102 รหัสผ่าน 14032022"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(866926077246832680)
        leave = guild.get_channel(937573869361979422)
        remove_player(member.id)
        await leave.send(f"{member.mention} : {member.name} ได้ออกจากเซิร์ฟของเราแล้ว")


def setup(bot):
    bot.add_cog(WelcomeCommands(bot))
