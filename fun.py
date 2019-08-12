from asyncio import sleep
import discord as dis
from discord.ext import commands as cmd
from uwu import uwu_word


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
    async def kick(self, ctx, member: dis.Member, *, reason="(no reason given)"):
        """Calls a vote on whether to kick a member"""
        message = await ctx.send('''*{} wants to call a vote:*
**Kick member: {}?**
**{}**
Press ✅ to vote YES
Press ❌ to vote NO
*Vote Count:*'''.format(ctx.author.display_name, member.display_name, reason))
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await sleep(50)
        await ctx.trigger_typing()
        await sleep(10)
        message = await ctx.channel.fetch_message(message.id)
        if message.reactions[0].count > message.reactions[1].count + 1:
            await ctx.send("✅ Vote Passed\nKicking member: " + member.display_name)
            for role in ctx.guild.roles:
                if role.name == "Kicked":
                    await member.add_roles(role, reason="Vote kick")
                elif role.name == "Member":
                    await member.remove_roles(role, reason="Vote kick")
        else:
            await ctx.send("❌ Vote Failed")


def setup(bot):
    bot.add_cog(Fun(bot))
