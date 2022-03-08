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
        em.add_field(name='Moderation', value='bank,dmbank,status,daily')
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
