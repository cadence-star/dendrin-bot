from discord.ext import commands as cmd


class Images(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command(name="HOW")
    async def how(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/569901396799913986/611290718266327097/image0.png")

    @cmd.command()
    async def haha(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/612097838146519061/612324381976166543/haha.jpg")

    @cmd.command()
    async def ifunny(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/612097838146519061/612324638621696030/ifunny1.jpg")

    @cmd.command()
    async def blocked(self, ctx):
        await ctx.send("https://media.discordapp.net/attachments/421449065704980482/611294597804458046/blocked.gif")

    @cmd.command(name="HMM")
    async def hmm(self, ctx):
        await ctx.send("https://media.discordapp.net/attachments/421449065704980482/605833714697633835/tenor_2.gif")

    @cmd.command()
    async def funny(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/612097838146519061/612325423262466048/funnyilaugh.png")

    @cmd.command()
    async def oktard(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/612097838146519061/612325813735653406/wryyytard.jpg")


def setup(bot):
    bot.add_cog(Images(bot))
