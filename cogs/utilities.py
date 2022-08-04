import time
import discord
import logging
import os
import sys
from datetime import datetime
from discord.ext import commands, tasks


embed = discord.Embed
guild = discord.Guild
user = discord.User
message = discord.Message
member = discord.Member


def     using_command_logging_info(context, message_content):
    return logging.info(f"Użytkownik {context.message.author} użył komendy <{message_content}>.")


def no_permission_logging_warning(username, message_content):
    return logging.warning(f"Użytkownik {username} próbwował próbował użyć komendy <{message_content}>,"
                           f"do której nie posiada uprawnień.")


def no_permission(username):
    msg = f"<@{username.id}>, niestety nie masz uprawnień do tego!"
    return msg


def deleting_message_logging_info(total_message, username, message_content):
    return logging.info(f"Usuwanie {total_message} wiadomości przez {username} używając komendy "
                        f"<{message_content}>")


def action_logging_warning(function, context, username_action, reason, delete_message_days=None, t=None):
    if function == "kick":
        t = "wyrzucił"
    if function == "ban":
        t = f"zbanował (usunięto wiadomości z {delete_message_days})"
    if function == "unban":
        t = "odbanował"
    if function == "mute":
        t = "zmutował"
    if function == "unmute":
        t = "odciszył"
    msg = f"Użytkownik {context.message.author} {t} {username_action.display_name} za: {reason}."
    return logging.warning(msg)


def user_no_exist(username):
    msg = f"<@{username.id}>, nie ma takiego użytkownika na serwerze."
    return msg


def user_no_exist_logging(username, message_content):
    return logging.error(f"Użytkownik {username} próbwował <{message_content}> użytkownikowi, którego  "
                         f"nie ma na serwerze.")


def wrong_uses(function, username, t=None):
    if function == "kick":
        t = f'!{function}'
    if function == "ban":
        t = f'!{function}'
    if function == "unban":
        t = f'!{function}'
    if function == "mute":
        t = f"!{function}"
    if function == "unmute":
        t = f"!{function}"
    msg = f'<@{username.id}>, źle użyłeś komendy, spróbuj `{t} <Użytkownik> <powód>`.'
    return msg


def wrong_uses_logging(function, username, message_content, t=None):
    if function == "kick":
        t = f"!{function}"
    if function == "ban":
        t = f"!{function}"
    if function == "unban":
        t = f"!{function}"
    if function == "mute":
        t = f"!{function}"
    if function == "unmute":
        t = f"!{function}"
    msg = f"Użytkownik {username} źle użył komendy <{t} {message_content}>."
    return logging.warning(msg)


def embed_action_info(function, ctx, username, bot, reason, what=None, what_happen=None):
    if function == "kick":
        what = "Wyrzucono z serwera!"
        what_happen = "wyrzucony z serwera"
    if function == "ban":
        what = "Zbanowano na serwerze!"
        what_happen = "zbanowany na serwerze"
    if function == "unban":
        what = "Odbanowano na serwerze!"
        what_happen = "odbanowany na serwerze"
    if function == "mute":
        what = "Wyciszono na serwerze!"
        what_happen = "wyciszony na serwerze"
    if function == "unmute":
        what = "Odciszono na serwerze!"
        what_happen = "odciszony na serwerze"

    embed_msg = embed(title=f"{what}",
                      description=f"Użytkownik {username} został {what_happen}.",
                      colour=discord.Colour.random())
    embed_msg.set_author(name=bot.name, icon_url=bot.avatar_url)
    embed_msg.timestamp = datetime.utcnow()
    embed_msg.set_thumbnail(url=username.avatar_url)
    embed_msg.add_field(name="Powód", value=reason, inline=False)
    embed_msg.add_field(name="Przez", value=ctx.message.author.mention, inline=False)
    embed_msg.set_footer(text=username.id)
    return embed_msg


def status_embed(status, bot, username, t=None, colour=None, thumbnail=None):
    if status == "aktywny":
        t = "*Aktywny* :green_circle:"
        colour = discord.Colour.green()
        thumbnail = "https://cdn.discordapp.com/attachments/944928580805201930/1002177380649021481/aktywny.png"
    if status == "prace":
        t = "*Prace techniczne* :yellow_circle:"
        colour = discord.Colour.from_rgb(255, 255, 0)
        thumbnail = "https://cdn.discordapp.com/attachments/944928580805201930/1002180084133806130/prace.png"
    if status == "przerwa":
        t = "*Przerwa*: :no_entry:"
        colour = discord.Colour.from_rgb(255, 0, 0)
        thumbnail = "https://cdn.discordapp.com/attachments/944928580805201930/1002179216210661446/przerwa.png"

    embed_msg = embed(title="",
                      description="",
                      colour=colour)
    embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
    embed_msg.set_thumbnail(url=thumbnail)
    embed_msg.add_field(name="Status", value=t)
    embed_msg.add_field(name="Ustawiony przez", value=username.mention)
    embed_msg.timestamp = datetime.utcnow()
    embed_msg.set_footer(text="RaDkon")
    return embed_msg


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        using_command_logging_info(ctx, ctx.message.content)
        bot = self.client.user
        embed_msg = embed(title="Restartowanie bota..",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.timestamp = datetime.utcnow()
        embed_msg.set_footer(text="")
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed_msg)
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)
        await ctx.channel.send(f"**Zostałem ponownie uruchomiony. Dzięki {ctx.message.author.mention}!**")

    @commands.command(name="list-users")
    @commands.has_permissions(administrator=True)
    async def list_of_users(self, ctx):
        using_command_logging_info(ctx, ctx.message.content)
        guild_server_id = ctx.channel.guild.id
        current_guild = self.client.get_guild(guild_server_id)
        members = [f"{member_guild.name}\n" for member_guild in current_guild.members]
        embed_msg = embed(title="Lista wszystkich użytkowników:",
                          description="".join(members),
                          colour=discord.Colour.from_rgb(96, 223, 213))
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed_msg)

    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        username = ctx.message.author.name
        msg_user_content = ctx.message.content
        await ctx.channel.purge(limit=1)
        messages_deleted = await ctx.channel.purge(limit=amount)
        total_deleted = len(messages_deleted)
        deleting_message_logging_info(total_deleted, username, msg_user_content)

    @clear.error
    async def clear_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            msg = no_permission(user_error)
            await ctx.channel.send(msg)

    @commands.command(name="clear-all")
    @commands.has_permissions(administrator=True)
    async def clear_all(self, ctx):
        username = ctx.message.author.name
        msg_user_content = ctx.message.content
        messages_deleted = await ctx.channel.purge()
        total_deleted = len(messages_deleted)
        deleting_message_logging_info(total_deleted, username, msg_user_content)

    @clear_all.error
    async def clear_all_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            msg = no_permission(user_error)
            await ctx.channel.send(msg)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, username: member, *, reason="brak powodu"):
        bot = self.client.user
        await ctx.channel.purge(limit=1)
        await username.kick(reason=reason)
        msg = embed_action_info("kick", ctx, username, bot, reason)
        await ctx.channel.send(embed=msg)
        action_logging_warning(function="kick", context=ctx, reason=reason, username_action=username)

    @kick.error
    async def kick_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR KICK: {error}")
        if isinstance(error, commands.MemberNotFound):
            user_no_exist_logging(user_error, msg_user_content)
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingRequiredArgument):
            wrong_uses_logging("kick", user_error, msg_user_content)
            text = wrong_uses("kick", user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            text = no_permission(user_error)
            await ctx.channel.send(text)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, username: member, *, reason="brak powodu", days=1):
        bot = self.client.user
        await ctx.channel.purge(limit=1)
        await username.ban(reason=reason, delete_message_days=days)
        msg = embed_action_info("ban", ctx, username, bot, reason)
        await ctx.channel.send(embed=msg)
        action_logging_warning(function="ban", context=ctx, reason=reason, username_action=username,
                               delete_message_days=days)

    @ban.error
    async def ban_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR BAN: {error}")
        if isinstance(error, commands.MemberNotFound):
            user_no_exist_logging(user_error, msg_user_content)
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingRequiredArgument):
            wrong_uses_logging("ban", user_error, msg_user_content)
            text = wrong_uses("ban", user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            text = no_permission(user_error)
            await ctx.channel.send(text)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, username, reason="brak powodu"):
        bot = self.client.user
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user_banned = ban_entry.user
            if str(username) in str(user_banned):
                username = user_banned
                await ctx.channel.purge(limit=1)
                await ctx.guild.unban(username, reason=reason)
                msg = embed_action_info("unban", ctx, username, bot, reason)
                await ctx.channel.send(embed=msg)
                action_logging_warning(function="unban", context=ctx, reason=reason, username_action=username)

    @unban.error
    async def unban_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR UNBAN: {error}")
        if isinstance(error, commands.UserNotFound):
            user_no_exist_logging(user_error, msg_user_content)
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingRequiredArgument):
            wrong_uses_logging("unban", user_error, msg_user_content)
            text = wrong_uses("unban", user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            text = no_permission(user_error)
            await ctx.channel.send(text)

    @commands.command(name="bans")
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        bot = self.client.user
        banned_users = await ctx.guild.bans()
        print(banned_users)
        if not banned_users:
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(f"<@{ctx.message.author.id}>, nie ma żadnych banów na serwerze :D")
        else:
            embed_msg = embed(title=f"Lista zbanowany użytkowników:",
                              description=f"",
                              colour=discord.Colour.red())
            embed_msg.set_author(name=bot.name, icon_url=bot.avatar_url)
            embed_msg.timestamp = datetime.utcnow()
            for ban_entry in banned_users:
                print(ban_entry.user, ban_entry.reason)
                embed_msg.add_field(name="Kto", value=ban_entry.user, inline=True)
                embed_msg.add_field(name="Powód", value=ban_entry.reason, inline=True)
            embed_msg.set_footer(text=len(banned_users))
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(embed=embed_msg)

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx, param):
        bot = self.client.user
        username = ctx.message.author
        if param == "aktywny":
            activity = discord.Game(name="Jest problem? !zglos")
            status_bot = discord.Status.online
            await self.client.change_presence(status=status_bot, activity=activity)
            embed_msg = status_embed(param, bot, username)
            await ctx.channel.purge(limit=2)
            await ctx.channel.send(embed=embed_msg)
            logging.info(f"Ustawiono status bota na: Aktywny.")
        if param == "prace":
            activity = discord.Game(name="RaDkon mnie naprawia :)))")
            status_bot = discord.Status.idle
            await self.client.change_presence(status=status_bot, activity=activity)
            embed_msg = status_embed(param, bot, username)
            embed_msg.set_footer(text="RaDkon")
            await ctx.channel.purge(limit=2)
            await ctx.channel.send(embed=embed_msg)
            logging.info(f"Ustawiono status bota na: Prace techniczne.")
        if param == "przerwa":
            activity = discord.Game(name="Mała przerwa..")
            status_bot = discord.Status.do_not_disturb
            await self.client.change_presence(status=status_bot, activity=activity)
            embed_msg = status_embed(param, bot, username)
            await ctx.channel.purge(limit=2)
            await ctx.channel.send(embed=embed_msg)
            logging.info(f"Ustawiono status bota na: Przerwa.")

    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def mute_member(self, ctx, username: member, *, reason="brak powodu"):
        bot = self.client.user
        guild_id = ctx.channel.guild.id
        current_guild = self.client.get_guild(guild_id)
        role_muted = current_guild.get_role(role_id=1002293617207034017)
        await ctx.channel.purge(limit=1)
        await username.add_roles(role_muted)
        msg = embed_action_info("mute", ctx, username, bot, reason)
        await ctx.channel.send(embed=msg)
        using_command_logging_info(ctx, ctx.message.content)

    @mute_member.error
    async def mute_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR UNBAN: {error}")
        if isinstance(error, commands.UserNotFound):
            user_no_exist_logging(user_error, msg_user_content)
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingRequiredArgument):
            wrong_uses_logging("mute", user_error, msg_user_content)
            text = wrong_uses("mute", user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            text = no_permission(user_error)
            await ctx.channel.send(text)

    @commands.command(name="unmute")
    @commands.has_permissions(administrator=True)
    async def unmute_member(self, ctx, username: member, *, reason="brak powodu"):
        bot = self.client.user
        guild_id = ctx.channel.guild.id
        current_guild = self.client.get_guild(guild_id)
        role_muted = current_guild.get_role(role_id=1002293617207034017)
        await ctx.channel.purge(limit=1)
        await username.remove_roles(role_muted)
        msg = embed_action_info("unmute", ctx, username, bot, reason)
        await ctx.channel.send(embed=msg)
        using_command_logging_info(ctx, ctx.message.content)

    @unmute_member.error
    async def mute_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR UNBAN: {error}")
        if isinstance(error, commands.UserNotFound):
            user_no_exist_logging(user_error, msg_user_content)
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingRequiredArgument):
            wrong_uses_logging("unmute", user_error, msg_user_content)
            text = wrong_uses("unmute", user_error)
            await ctx.channel.send(text)
        if isinstance(error, commands.MissingPermissions):
            no_permission_logging_warning(user_error, msg_user_content)
            text = no_permission(user_error)
            await ctx.channel.send(text)



def setup(client):
    client.add_cog(Moderation(client))
