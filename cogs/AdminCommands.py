# AdminCommands.py
from discord.ext import commands
from store.store_db import reset_stock, get_item_id

class AdminCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name='update')
	@commands.has_permission(manage_roles=True)
	async def upate_command(self, ctx, arg: str, arg1: int):
		if get_item_id(arg) is not None:
			update = reset_stock(arg, arg1)
			await ctx.reply(update, mention_author=False)
		elif get_item_id(arg) is None:
			await ctx.reply(f'ไม่พบข้อมูล item {arg} ในระบบ', mention_author=False)


	@upate_command.error
	async def update_comman_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
            await ctx.reply('⚠ Error, **For Admin only**')
            return None
        elif isinstance(error, commands.MissingRequiredArgument):
        	await ctx.reply('Mission a reqiured argument : {}'.format(error.param))
		




def setup(bot):
	bot.add_cog(AdminCommands(bot))