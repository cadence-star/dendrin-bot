import discord as dis
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

    @cfg.group(name="kick")
    async def kick(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `;cfg kick setup` to set up the kick command.")

    @kick.command()
    async def setup(self, ctx):
        for role in ctx.guild.roles:
            await role.update(read_messages=False)
        role1 = await ctx.guild.create_role(
            name="Member", permissions=dis.Permissions(1024), reason="Kick command setup")
        for member in ctx.guild.members:
            await member.add_roles(role1, "Kick command setup")
        role2 = await ctx.guild.create_role(name="Kicked", reason="Kick command setup")
        await ctx.guild.create_text_channel("kick-zone", overwrites={
            ctx.guild.default_role: dis.PermissionOverwrite(read_messages=False),
            role2: dis.PermissionOverwrite(read_messages=True)}, reason="Kick command setup")

    @cmd.command()
    async def leave(self, ctx):
        """Makes the bot leave the server"""
        await ctx.send("oof")
        await ctx.guild.leave()


def setup(bot):
    bot.add_cog(Admin(bot))
