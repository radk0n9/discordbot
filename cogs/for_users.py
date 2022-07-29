import discord
import logging
import requests
from datetime import datetime
from discord.ext import commands
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import desc

embed = discord.Embed
guild = discord.Guild
user = discord.User
message = discord.Message
member = discord.Member


def now_time():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return date_time


def random_mem():
    response = requests.get(url="https://ivall.pl/memy")
    response.raise_for_status()
    data = response.json()
    return data["url"]


def reset_cooldown(ctx):
    if ctx.message.author.id == 287292834355347456:
        return ctx.command.reset_cooldown(ctx)


def info_embed(ctx, username):
    username_created_at = username.created_at.strftime("%d-%m-%Y")
    username_name = username.display_name
    username_avatar = username.avatar_url
    username_joined_at = username.joined_at.strftime("%d-%m-%Y")
    username_status = str(username.status).title()

    members = sorted(ctx.guild.members, key=lambda member_join: member_join.joined_at)
    username_join_position = members.index(username) + 1

    # permission = [str(perm[0]).replace("_", " ").title() for perm in username.guild_permissions if perm[1]]
    # permission_string = ", ".join(permission)

    embed_msg = embed(title="Informacje o koncie",
                      description="",
                      colour=discord.Colour.random())
    embed_msg.set_author(name=username_name, icon_url=username_avatar)
    embed_msg.timestamp = datetime.utcnow()
    embed_msg.set_thumbnail(url=username_avatar)
    embed_msg.add_field(name="Status", value=username_status, inline=False)
    embed_msg.add_field(name="Pełna nazwa konta", value=username, inline=False)
    embed_msg.add_field(name="Data utworzenia konta", value=username_created_at, inline=False)
    embed_msg.add_field(name="Data dołączenia na serwer", value=username_joined_at, inline=False)
    embed_msg.add_field(name="Dołączył do sewera jako", value=username_join_position, inline=False)
    if len(username.roles) > 1:
        role_string = " ".join([role.mention for role in username.roles[1:]])
        embed_msg.add_field(name=f"Role [{len(username.roles) - 1}]", value=role_string, inline=False)
    embed_msg.set_footer(text=username.id)
    return embed_msg


def user_no_exist(username):
    msg = f"<@{username}>, nie ma takiego użytkownika na serwerze."
    return msg


def user_no_exist_logging(username, message_content):
    return logging.error(f"Użytkownik {username} próbwował <{message_content}> użytkownikowi, którego  "
                         f"nie ma na serwerze.")


def using_command_logging_info(context, message_content):
    return logging.info(f"Użytkownik {context.message.author} użył komendy <{message_content}>.")


def wrong_uses(function, username, t=None):
    if function == "zglos":
        t = f'!{function} propozycja/problem/bug'
    if function == "ping":
        t = f'!{function} @NazwaUżytkownika'
    msg = f"<@{username.id}>, spóbuj użyć: `{t}`."
    return msg


def wrong_uses_logging(function, username, message_content, t=None):
    if function == "zlos":
        t = f"!{function}"
    if function == "ping":
        t = f"!{function}"
    msg = f"Użytkownik {username} źle użył komendy <`{t}` {message_content}>."
    return logging.warning(msg)


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/konradpawelec/PycharmProjects/discordbot/messages-ranking.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\konra\\discordbot\\messages-ranking.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)


class ForUsers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="zglos")
    @commands.has_permissions(send_messages=True)
    async def report_a_problem(self, ctx, *, problem):
        channel_problemy = self.client.get_channel(996485249989103616)
        # channel = ctx.channel.id
        username = ctx.message.author
        bot = self.client.user
        embed_msg = embed(title="Dziękuję za zgłoszenie :)",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.set_thumbnail(url=username.avatar_url)
        embed_msg.add_field(name="Treść", value=problem)
        embed_msg.add_field(name="Zgłoszone przez", value=username.mention)
        embed_msg.set_footer(text="zglos")
        embed_msg.timestamp = datetime.utcnow()
        msg = await ctx.send(embed=embed_msg)
        emojis = ["👍", "👎"]
        for emoji in emojis:
            await msg.add_reaction(emoji=emoji)
        await channel_problemy.send(f"**Problem/Bug/Propozycja:**\n"
                                    f"\n{problem}\n"
                                    f"\nZgłoszone przez <@{username.id}>")
        using_command_logging_info(ctx, ctx.message.content)

    @report_a_problem.error
    async def report_a_problem_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        if isinstance(error, commands.MissingRequiredArgument):
            msg = wrong_uses("zglos", user_error)
            await ctx.channel.send(msg)
            wrong_uses_logging("zglos", user_error, msg_user_content)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="ping")
    @commands.has_permissions(send_messages=True)
    async def ping(self, ctx, username: member, *, message="*brak wiadomości*"):
        reset_cooldown(ctx)
        pinger = ctx.message.author
        avatar_pinger = ctx.author.avatar_url
        await ctx.channel.purge(limit=1)
        embed_msg = embed(title="PING!",
                          description=f"Dostałeś **PING'a** od użytkownika **{pinger.name}**!\n\n",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=pinger.name, icon_url=avatar_pinger)
        embed_msg.timestamp = datetime.utcnow()
        embed_msg.set_footer(text="PING")
        embed_msg.set_thumbnail(url=avatar_pinger)
        embed_msg.add_field(name="Wiadomość", value=message, inline=False)
        embed_msg.add_field(name="Serwer", value=self.client.get_guild(944920041361661952).name, inline=False)
        channel = await username.create_dm()
        await channel.send(embed=embed_msg)

    @ping.error
    async def ping_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR PING: {error}")
        if isinstance(error, commands.MissingRequiredArgument):
            text = wrong_uses("ping", user_error)
            await ctx.channel.send(text)
            wrong_uses_logging("ping", user_error, msg_user_content)
        if isinstance(error, commands.MemberNotFound):
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
            user_no_exist_logging(user_error, msg_user_content)
        if isinstance(error, commands.CommandOnCooldown):
            text = f"<@{user_error.id}>, spokojnie spokojnie, nie spiesz się tak z tym :D. Spróbuj ponownie za {error.retry_after:.2f}s"
            await ctx.channel.send(text)
            logging.error(f"Użytkownik {user_error} chciał za szybko użyć komendy <!ping {msg_user_content}>")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="komendy")
    @commands.has_permissions(send_messages=True)
    async def komendy(self, ctx):
        reset_cooldown(ctx)
        bot = self.client.user
        msg_user_content = ctx.message.content
        embed_msg = embed(title="Dostępne komendy na serwerze:",
                          description="`!zglos <propozycja/problem/bug` - jeśli chcesz coś zaproponować lub"
                                      " zgłosić problem/buga użyj tej komendy\n\n"
                                      "`!ping @NazwaUżytkownika` - umożliwa pingowanie użytownika "
                                      "(proszę nie nadużywać :))\n\n"
                                      "`!losowy-mem` - umożliwia wysłanie losowego mema ze strony memy.pl\n\n"
                                      "`!info` - możesz sprawdzić informacje o sobie lub o innych użytkownikach np."
                                      " !info @NazwaUżytkownika\n\n"
                                      "`!ranking` - wyświetla ranking wysłanych wiadomości na serwerze\n\n"
                                      "`...` - ...\n\n"
                                      "*kiedyś będzie ich więcej..*",
                          colour=discord.Colour.from_rgb(96, 223, 213))
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.set_thumbnail(url=bot.avatar_url)
        embed_msg.set_footer(text="komendy")
        embed_msg.timestamp = datetime.utcnow()
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed_msg)
        using_command_logging_info(ctx, msg_user_content)

    @komendy.error
    async def komendy_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user = ctx.message.content
        logging.error(f"ERROR KOMENDY: {error}")
        if isinstance(error, commands.CommandOnCooldown):
            text = f"<@{user_error.id}>, ejj ty, czemu tak nadużywasz tej komendy? Poczekaj {error.retry_after:.2f}s i spróbuj ponownie."
            await ctx.channel.send(text)
            logging.error(f"Użytkownik {user_error} chciał za szybko użyć komendy !komendy ({msg_user})")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="losowy-mem")
    @commands.has_permissions(send_messages=True)
    async def losowy_mem(self, ctx):
        reset_cooldown(ctx)
        username = ctx.message.author
        msg_user_content = ctx.message.content
        channel_mems = self.client.get_channel(int(1000405621444710460))
        if channel_mems.name == ctx.channel.name:
            await ctx.channel.purge(limit=1)
            mem = random_mem()
            msg = await channel_mems.send(mem)
            emojis = ["🤣", "🥱"]
            for emoji in emojis:
                await msg.add_reaction(emoji)
            using_command_logging_info(ctx, msg_user_content)
        else:
            await ctx.channel.send(f"<@{username.id}>, używasz złego kanału. Przejdź na <#{channel_mems.id}>")
            logging.warning(f"{username} użył złego kanału do wysłania mema (#{ctx.channel.name})")

    @losowy_mem.error
    async def losowy_mem_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user = ctx.message.content
        logging.error(f"ERROR LOSOWY-MEM: {error}")
        if isinstance(error, commands.CommandOnCooldown):
            text = f"<@{user_error.id}>, poczekaj jeszcze chwilkę, dawka nowych memów już za: {error.retry_after:.2f}s."
            await ctx.channel.send(text)
            logging.error(f"Użytkownik {user_error} chciał za szybko użyć komendy !losoyw-mem ({msg_user})")

    @commands.command(name="info")
    @commands.has_permissions(send_messages=True)
    async def info_about(self, ctx, *, username: member = " "):
        msg_user_content = ctx.message.content
        if not username == " ":
            embed_message = info_embed(ctx, username)
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(f"<@{ctx.author.id}>")
            await ctx.channel.send(embed=embed_message)
            using_command_logging_info(ctx, msg_user_content)
        else:
            username = ctx.author
            embed_message = info_embed(ctx, username)
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(f"<@{username.id}>")
            await ctx.channel.send(embed=embed_message)
            using_command_logging_info(ctx, msg_user_content)

    @info_about.error
    async def info_error(self, ctx, error):
        user_error = ctx.message.author
        msg_user_content = ctx.message.content
        logging.error(f"ERROR INFO-ABOUT: {error}")
        if isinstance(error, commands.MemberNotFound):
            text = user_no_exist(user_error)
            await ctx.channel.send(text)
            user_no_exist_logging(user_error, msg_user_content)

    @commands.command(name="ranking")
    @commands.has_permissions(send_messages=True)
    async def ranking(self, ctx):
        bot = self.client.user
        query_message = db.session.query(Messages)
        sorting_desc = desc(Messages.value)
        order_by_value = query_message.order_by(sorting_desc)
        embed_msg = embed(title="Ranking wysłanych wiadomość",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.timestamp = datetime.utcnow()
        embed_msg.set_footer(text=f"{len(Messages.query.all())}")
        ids = [result.id_user for result in order_by_value]
        id_for_mention = [self.client.get_user(u_id).mention for u_id in ids]
        value = [f"{result.value}\n"for result in order_by_value]
        embed_msg.add_field(name="Użytkownik", value="\n".join(id_for_mention), inline=True)
        embed_msg.add_field(name="Liczba wiadomości", value=" ".join(value), inline=True)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed_msg)

    # @ranking.error
    # async def ranking_error(self, ctx, error):
    #     user_error = ctx.message.author
    #     msg_user_content = ctx.message.content
    #     logging.error(f"ERROR INFO-ABOUT: {error}")
    #     if isinstance(error, commands.MemberNotFound):
    #         text = user_no_exist(user_error)
    #         await ctx.channel.send(text)
    #         user_no_exist_logging(user_error, msg_user_content)


def setup(client):
    client.add_cog(ForUsers(client))
