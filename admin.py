import sqlite3
import discord as dis
from discord.ext import commands as cmd
import helpers


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
            await helpers.handle_default(ctx, error)

    @cfg.group(name="kick")
    async def kick(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `;cfg kick setup` to set up the kick command.")

    @kick.command()
    @cmd.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def setup(self, ctx):
        ctx.send("Setting up...")
        reason = "Kick command setup"

        # remove read_messages perm from every role
        for role in ctx.guild.roles:
            try:
                perms = role.permissions
                perms.update(read_messages=False)
                await role.edit(permissions=perms, reason=reason)
            except dis.Forbidden:
                pass

        # create member role with read_messages perm
        member_role = await ctx.guild.create_role(
            name="Member", permissions=dis.Permissions(1024), reason=reason)

        # add member role to everyone
        for member in ctx.guild.members:
            await member.add_roles(member_role, reason=reason)

        # create kicked role without read_messages perm
        kicked_role = await ctx.guild.create_role(name="Kicked", reason=reason)

        # give kicked role to self to allow viewing the kick channel
        await ctx.guild.me.add_roles(kicked_role, reason=reason)

        # create kick channel that only users with the kicked role can see
        kick_channel = await ctx.guild.create_text_channel("kick-zone", overwrites={
            ctx.guild.default_role: dis.PermissionOverwrite(read_messages=False),
            kicked_role: dis.PermissionOverwrite(read_messages=True)}, reason=reason)

        # save ids to database
        con = sqlite3.connect("guild.db")
        con.execute("UPDATE guild SET member_role=?, kicked_role=?, kick_channel=? WHERE id=?",
                    (member_role.id, kicked_role.id, kick_channel.id, ctx.guild.id))
        con.commit()
        con.close()

        ctx.send("Done!")

    @kick.error
    async def kick_err(self, ctx, error):
        if isinstance(error, cmd.BotMissingPermissions):
            await ctx.send(
                'Error: I must have the "Manage Roles" and "Manage Channels" permissions to run this command.')
        else:
            await helpers.handle_default(ctx, error)

    @kick.command()
    async def teardown(self, ctx):
        ctx.send("Tearing down...")
        reason = "Kick command teardown"

        # get ids from database and remove
        con = sqlite3.connect("guild.db")
        ids = con.execute("SELECT member_role, kicked_role, kick_channel FROM guild WHERE id=?",
                          ctx.guild.id).fetchone()
        if ids is None:
            ctx.send("The kick command is not set up in this server!")
            con.close()
            return
        con.execute("UPDATE guild SET member_role=?, kicked_role=?, kick_channel=? WHERE id=?",
                    (None, None, None, ctx.guild.id))
        con.commit()
        con.close()

        # add read_messages perm to @everyone
        perms = ctx.guild.default_role.permissions
        perms.update(read_messages=True)
        await ctx.guild.default_role.edit(permissions=perms, reason=reason)

        # delete everything
        await ctx.guild.get_channel(ids[2]).delete(reason=reason)
        await ctx.guild.get_role(ids[1]).delete(reason=reason)
        await ctx.guild.get_role(ids[0]).delete(reason=reason)

        ctx.send("Done!")

    @cmd.command()
    async def leave(self, ctx):
        """Makes the bot leave the server"""
        await ctx.send("oof")
        await ctx.guild.leave()

    @cmd.command()
    @cmd.is_owner()
    async def upgrade(self, ctx):
        # temp command for existing guilds
        con = sqlite3.connect("guild.db")
        con.execute("INSERT INTO guild (id) VALUES (?)")
        con.commit()
        con.close()
        ctx.send("Successfully upgraded guild")


def setup(bot):
    bot.add_cog(Admin(bot))
