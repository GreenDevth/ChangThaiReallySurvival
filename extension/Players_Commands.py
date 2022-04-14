import discord
import requests
import json
from discord.ext import commands

from database.Member_db import member_check, player_info


class PlayerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server')
    @commands.has_role("Verify Members")
    async def server_command(self, ctx):
        response = requests.get("https://api.battlemetrics.com/servers/13458708")
        res_text = response.text
        json.loads(res_text)
        json_obj = response.json()
        scum_server = json_obj['data']['attributes']['name']
        scum_ip = json_obj['data']['attributes']['ip']
        scum_port = json_obj['data']['attributes']['port']
        scum_player = json_obj['data']['attributes']['players']
        scum_player_max = json_obj['data']['attributes']['maxPlayers']
        scum_rank = json_obj['data']['attributes']['rank']
        scum_status = json_obj['data']['attributes']['status']
        scum_time = json_obj['data']['attributes']['details']['time']
        scum_version = json_obj['data']['attributes']['details']['version']
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == 925559937323659274 or role in ctx.author.roles:
            await ctx.reply(
                "📃 **SERVER INFORMATION DATA**"
                "```============================================="
                f"\nServer: {scum_server} "
                f"\nIP: {scum_ip}:{scum_port} "
                f"\nStatus: {scum_status} "
                f"\nTime in Game: {scum_time} "
                f"\nPlayers: {scum_player}/{scum_player_max} "
                f"\nRanking: #{scum_rank} "
                f"\nGame version: {scum_version}\n "
                f"\nServer Restarts Every 6 hours "
                f"\nDay 3.8 hours, Night 1 hours\n"
                f"=============================================```",
                mention_author=False
            )
        else:
            await ctx.reply("กรุณาพิมพ์คำสั่งนี้ที่้ห้อง <#925559937323659274> เท่านั้น", mention_author=False, delete_after=5)
        await ctx.message.delete()

    @server_command.error
    async def server_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#878878305296728095>',
                            mention_author=False)
            await ctx.message.delete()

    @commands.command(name='status')
    @commands.has_role("Verify Members")
    async def status_command(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == 925559937323659274 or role in ctx.author.roles:
            member = ctx.author
            check = member_check(member.id)
            if check == 1:
                player = player_info(member.id)
                coins = "${:,d}".format(player[5])
                member.created_at.strftime("%b %d, %Y")
                joined_at = member.joined_at.strftime("%b %d, %Y")
                await ctx.reply(
                    content="📖 **YOUR PLAYER INFORMATION**\n"
                            "```cs\n"
                            "========================================\n"
                            f"Discord Name : '{player[1]}'\n"
                            f"Discord ID : {player[2]}\n"
                            f"Steam ID : {player[3]}\n"
                            f"Bank ID : {player[4]}\n"
                            f"Bank Balance : {coins}\n"
                            f"Level : {player[6]}\n"
                            f"Exp : {player[7]}\n"
                            f"Join server at : '{joined_at}'\n"
                            "========================================"
                            "\n```",
                    mention_author=False
                )
            else:
                await ctx.reply(content='⚠ Error, your account ID not found!')
        else:
            await ctx.reply("กรุณาพิมพ์คำสั่งนี้ที่้ห้อง <#925559937323659274> เท่านั้น", mention_author=False, delete_after=5)
        await ctx.message.delete()

    @status_command.error
    async def status_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#878878305296728095>',
                            mention_author=False)
            await ctx.message.delete()

    @commands.command(name='dmbank')
    @commands.has_role("Verify Members")
    async def dmbank_command(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == 925559937323659274 or role in ctx.author.roles:
            member = ctx.author
            check = member_check(ctx.author.id)
            if check == 1:
                player = player_info(member.id)
                coins = "${:,d}".format(player[5])
                await discord.DMChannel.send(
                    member,
                    f'Account Name : {player[1]}\n'
                    f'Bank ID : {player[4]}\n'
                    f'Bank Balance : {coins}'
                )
                await ctx.reply('Bank statements are being delivered to your inbox.',
                                mention_author=False)
            else:
                await ctx.reply('⚠ Error, your account ID not found!')
        else:
            await ctx.reply("กรุณาพิมพ์คำสั่งนี้ที่้ห้อง <#925559937323659274> เท่านั้น", mention_author=False, delete_after=5)
        await ctx.message.delete()

    @dmbank_command.error
    async def dmbank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#878878305296728095>',
                            mention_author=False)
            await ctx.message.delete()

    @commands.command(name='bank')
    @commands.has_role("Verify Members")
    async def bank_command(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        if ctx.channel.id == 925559937323659274 or role in ctx.author.roles:
            check = member_check(ctx.author.id)
            if check == 1:
                player = player_info(ctx.author.id)
                coins = "${:,d}".format(player[5])
                await ctx.reply(
                    "📖 **YOUR PLAYER BANK STATEMENT**"
                    '```css\n'
                    f'Account name : "{player[1]}", '
                    f'Bank ID : {player[4]}, '
                    f'Bank Balance : {coins}'
                    '\n```',
                    mention_author=False
                )
            else:
                await ctx.reply('⚠ Error, your account ID not found!')
        else:
            await ctx.reply("กรุณาพิมพ์คำสั่งนี้ที่้ห้อง <#925559937323659274> เท่านั้น", mention_author=False, delete_after=5)
        await ctx.message.delete()

    @bank_command.error
    async def bank_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply('You have not verified your membership. Please visit <#878878305296728095>',
                            mention_author=False)
            await ctx.message.delete()
