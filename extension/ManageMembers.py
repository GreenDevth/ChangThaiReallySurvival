import discord
import datetime
from discord.ext import commands
from database.Member_db import new_player, remove_player


class JoinServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(866926077246832680)
        welcome = guild.get_channel(914080006429360149)
        role = discord.utils.get(guild.roles, name='joiner')
        await member.add_roles(role)
        discord_id = str(member.id)
        bank_id = discord_id[:5]
        name = str(member.name)
        x = datetime.datetime.now()
        join_date = x.strftime("%d/%m/%Y %H:%M:%S")

        result = new_player(name, int(member.id), bank_id, join_date)
        await welcome.send(f'{member.mention} : {member.name} ได้เข้าร่วมดิสคอร์สของเราแล้ว')

        """ Send DM to Joiner member """
        await discord.DMChannel.send(
            member,
            result
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(866926077246832680)
        leave = guild.get_channel(937573869361979422)
        remove_player(member.id)
        await leave.send(f"{member.mention} : {member.name} ได้ออกจากเซิร์ฟของเราแล้ว")
