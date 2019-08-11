from asyncio import sleep
import discord as dis
from discord.ext import commands as cmd
import logging
from jishaku.help_command import DefaultPaginatorHelp
from uwu import uwu_word
from secret import token
import helpers

logging.basicConfig(level=logging.INFO)
bot = cmd.Bot(command_prefix=';', help_command=DefaultPaginatorHelp(),
              activity=dis.Activity(name=";help", type=dis.ActivityType.watching))
bot.load_extension('jishaku')
bot.load_extension('admin')


@bot.command()
async def uwu(ctx, *, text):
    """Change any text to UwU-speak"""
    text = text.replace("fuck", "fwick").replace("shit", "poopoo").replace("bitch", "meanie").replace(
        "ass", "butt").replace("father", "daddy")
    await ctx.send(' '.join([await uwu_word(word) for word in text.lower().split()]))


@bot.command()
@cmd.guild_only()
async def kick(ctx, member: dis.Member, *, reason="(no reason given)"):
    """Calls a vote on whether to kick a member"""
    message = await ctx.send('''*{} wants to call a vote:*
**Kick member: {}?**
**{}**
Press ✅ to vote YES
Press ❌ to vote NO
*Vote Count:*'''.format(ctx.author.display_name, member.display_name, reason))
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    await sleep(590)
    await ctx.trigger_typing()
    await sleep(10)
    message = await ctx.channel.fetch_message(message.id)
    if message.reactions[0].count > message.reactions[1].count:
        await ctx.send("✅ Vote Passed\nKicking member: " + member.display_name)
        for role in ctx.guild.roles:
            if role.name == "Kicked":
                await member.add_roles(role, reason="Vote kick")
            elif role.name == "Member":
                await member.remove_roles(role, reason="Vote kick")
    else:
        await ctx.send("❌ Vote Failed")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, cmd.CommandNotFound):
        await ctx.send("Error: Command not found")
    else:
        helpers.handle_default(ctx, error)

bot.run(token)
