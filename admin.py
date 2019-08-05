from discord.ext import commands as cmd


class Admin(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.guild_permissions.administrator or ctx.author.id == 363424348742352906:
            return True
        for role in ctx.author.roles:
            if role.name == "Bot Manager":
                return True
        return False

    @cmd.group()
    @cmd.guild_only()
    async def cfg(self, ctx):
        """Change the settings on a command"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Command does not exist or is not configurable.")

    @cfg.error
    async def cfg_err(self, ctx, error):
        if isinstance(error, cmd.CheckFailure):
            await ctx.send(
                "You must have the Administrator permission or a role called \"Bot Manager\" to use this command.")
        else:
            await ctx.send(error)

    @cfg.command(name="kick")
    async def cfg_kick(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))
