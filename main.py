import discord as dis
from discord.ext import commands as cmd
import logging
from jishaku.help_command import DefaultPaginatorHelp
from secret import token
import helpers

logging.basicConfig(level=logging.INFO)
bot = cmd.Bot(command_prefix=';', help_command=DefaultPaginatorHelp(),
              activity=dis.Activity(name=";help", type=dis.ActivityType.watching))
bot.load_extension('jishaku')
bot.load_extension('fun')
bot.load_extension('admin')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, cmd.CommandNotFound):
        await ctx.send("Error: Command not found")
    else:
        await helpers.handle_default(ctx, error)

bot.run(token)

