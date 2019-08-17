from discord.ext import commands as cmd


class Images(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command(name="HOW")
    async def how(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/569901396799913986/611290718266327097/image0.png")


def setup(bot):
    bot.add_cog(Images(bot))
