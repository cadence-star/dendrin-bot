import random
import sqlite3
from asyncio import sleep
import discord as dis
from discord.ext import commands as cmd
import helpers


class Fun(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command()
    async def uwu(self, ctx, *, text):
        """Change any text to UwU-speak"""
        text = text.replace("fuck", "fwick").replace("shit", "poopoo").replace("bitch", "meanie").replace(
            "ass", "butt").replace("father", "daddy").replace("god", "gosh").replace("damn", "darn").replace(
            "idiot", "dumb-face")
        await ctx.send(' '.join([await uwu_word(word) for word in text.lower().split()]))

    @cmd.command()
    @cmd.guild_only()
    @cmd.bot_has_permissions(add_reactions=True)
    async def kick(self, ctx, member: dis.Member, *, reason="(no reason given)"):
        """Calls a vote on whether to kick a member"""

        # get vote time from database
        con = sqlite3.connect("guild.db")
        time = con.execute("SELECT kick_vote_time FROM guild WHERE id=?", (ctx.guild.id,)).fetchone()[0]
        con.close()

        # call vote
        message = await ctx.send('''*{} wants to call a vote:*
**Kick member: {}?**
**{}**
Press ✅ to vote YES
Press ❌ to vote NO
*Vote Count:*'''.format(ctx.author.display_name, member.display_name, reason))
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        # wait default 1 minute
        await sleep((time or 60) - 10)
        await ctx.trigger_typing()
        await sleep(10)

        # get updated message with reactions from server
        message = await ctx.channel.fetch_message(message.id)

        # vote passes if there are at least 2 more checks than Xs
        if message.reactions[0].count > message.reactions[1].count:
            await ctx.send("✅ Vote Passed\nKicking member: " + member.display_name)

            # get info from database
            con = sqlite3.connect("guild.db")
            ids = con.execute("SELECT member_role, kicked_role FROM guild WHERE id=?", (ctx.guild.id,)).fetchone()
            con.close()

            # don't do anything if kick has not been set up in this guild
            if None in ids:
                return

            # send member to kick channel
            try:
                await member.add_roles(ctx.guild.get_role(ids[1]), reason="Vote kick")
                await member.remove_roles(ctx.guild.get_role(ids[0]), reason="Vote kick")
            except dis.Forbidden:
                pass
        else:
            await ctx.send("❌ Vote Failed")


def setup(bot):
    bot.add_cog(Fun(bot))


async def uwu_word(word):
    end = ''
    veryEnd = ''

    # ignore non-letter endings
    prefix = True
    for i in range(len(word)):
        if prefix and word[i].isalpha():
            prefix = False
        elif not prefix and not word[i].isalpha():
            veryEnd = word[i:]
            word = word[:i]
            break

    # randomly change punctuation to kaomoji
    if word[-1] in ',.?!':
        end = word[-1]
        word = word[:-1]
        if end in ',.':
            chance = 0.33
        else:
            chance = 0.50
        if random.random() < chance:
            if end == ',':
                end = random.choice(
                    [" (⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)..", " (\\*^.^\\*)..,", "..,", ",,,", "... ", ".. ", " mmm..", "O.o"])
            elif end == '?':
                end = random.choice(
                    [" (o_O)?", " (°ロ°) !?", " (ーー;)?", " owo?"])
            else:
                end = random.choice(
                    [" (\\* ^ ω ^)", " (o^▽^o)", " (≧◡≦)", " ☆⌒ヽ(\\*\"､^\\*)chu", " ( ˘⌣˘)♡(˘⌣˘ )", " xD"])
        if random.random() < 0.25:
            end = random.choice(
                [" \\*:･ﾟ✧\\*:･ﾟ✧ ", " ☆\\*:・ﾟ ", "〜☆ ", " uguu.., ", "-.-"])

    # don't change some endings
    if word.endswith(('le', 'll', 'er', 're')):
        end = word[-2:] + end
        word = word[:-2]
    elif word.endswith(('les', 'lls', 'ers', 'res')):
        end = word[-3:] + end
        word = word[:-3]

    # uwu
    word = word.replace('l', 'w').replace('r', 'w') + end + veryEnd

    # random stutter
    if len(word) > 2 and word[0].isalpha() and random.random() < 0.17:
        word = word[0] + '-' + word
    return word
