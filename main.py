from importlib import reload
import sqlite3
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
bot.load_extension('images')
bot.load_extension('admin')


@bot.command(name="reloadhelpers", hidden=True)
@cmd.is_owner()
async def reload_helpers(ctx):
    reload(helpers)
    ctx.send("🔁 `helpers`")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, cmd.CommandNotFound):
        await ctx.send("Error: Command not found")
    else:
        await helpers.handle_default(ctx, error)


@bot.event
async def on_guild_join(guild):
    con = sqlite3.connect('guild.db')
    con.execute("INSERT INTO guild (id) VALUES (?)", (guild.id,))
    con.commit()
    con.close()


@bot.event
async def on_member_join(member):
    con = sqlite3.connect('guild.db')
    roleID = con.execute("SELECT member_role FROM guild WHERE id=?", (member.guild.id,)).fetchone()[0]
    con.close()
    if roleID is not None:
        await member.add_roles(member.guild.get_role(roleID))

bot.run(token)
