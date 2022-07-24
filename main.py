# TODO 1  twitch stream notification
# TODO 2 MEE6 check some new features
# TODO 3 Creating channel for someone

import discord
import sys
import requests
from datetime import datetime
import os
import logging
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET
from rich.logging import RichHandler
from my_client import MyClient
from event import SendMessage, OnMember, OnMemberUpdate
from discord.ext.commands import has_permissions, MissingPermissions, MemberNotFound, MissingRequiredArgument, cooldown,\
    BucketType, CommandOnCooldown, CommandInvokeError
from discord.errors import HTTPException


rich_handler: RichHandler = RichHandler(rich_tracebacks=True)
rich_handler.setLevel(INFO)
rich_handler.setFormatter(Formatter("%(message)s"))

if not os.path.isdir('./Log'):
   os.makedirs('./Log', exist_ok=True)
file_handler = FileHandler(
   f"./Log/log{datetime.now():_%d-%m-%Y_%H-%M-%S-%f}.log", encoding="utf-8")

file_handler.setLevel(DEBUG)
file_handler.setFormatter(
    Formatter("%(asctime)s@ %(name)s [%(levelname)s] %(funcName)s: %(message)s"))

logging.basicConfig(level=NOTSET, handlers=[rich_handler, file_handler])

intents = discord.Intents.all()
intents.members = True
client = MyClient(command_prefix="!", intents=intents, self_bot=False)

embed = discord.Embed
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


# Clearing chat command (!clear <amount> and !clear-all
client.clearing()

# Reporting a problem experienced by user (!zglos <problem>)
client.report_a_problem()

# Changing status of bot and current activity using commands (!status <aktywny, prace-techniczne, przerwa>)
client.status_of_bot()

# Adding roles users using reactions below message which bot sent
client.reaction_role_chanel()

# Moderate section
client.moderate()

@client.event
async def on_message(msg):
    channel = msg.channel

    send_message = SendMessage(msg)
    content = send_message.text_hi()
    try:
        await msg.channel.send(content)
    except discord.errors.HTTPException:
        pass

    try:
        message_attachments = msg.attachments[0]
        filename = message_attachments.filename
        url = message_attachments.url
        if channel.name == "🔮・mems":
            if "https://" in msg.content or "http://" in msg.content or msg.attachments:
                emojis = ["🤣", "🥱"]
                for emoji in emojis:
                    await msg.add_reaction(emoji)

                logging.info(f"Dodano reakcje: {emojis} do wiadomości {msg.author.name} o treści <{msg.content},"
                             f" nazwa pliki: {filename}, link do pliku: {url}> na kanale: {channel}")
    except IndexError:
        logging.info(f"\n\n{msg.author.name} wysłał wiadomość: <{msg.content}> na kanale: {channel}.\n")

    await client.process_commands(msg)


@client.event
async def on_member_join(member):
    on_member = OnMember(member)
    channel = client.get_channel(int(on_member.channel("witaj_i_zegnaj")))
    msg = on_member.when_member_join()
    await channel.send(msg)


@client.event
async def on_member_remove(member):
    on_member = OnMember(member)
    channel = client.get_channel(int(on_member.channel("witaj_i_zegnaj")))
    msg = on_member.when_member_leave()
    await channel.send(msg)


@client.event
async def on_member_update(before, after):
    member = ""
    on_member = OnMember(member)
    on_member_update_boost = OnMemberUpdate(before, after)
    if len(before.roles) < len(after.roles):
        new_role = next(role for role in after.roles if role not in before.roles)
        channel = client.get_channel(int(on_member.channel("chat")))
        if new_role.name == "Server Booster":
            msg = on_member_update_boost.when_member_boost_server()
            await channel.send(msg)


@cooldown(1, 30, BucketType.user)
@client.command(name="ping")
@has_permissions(send_messages=True)
async def ping(ctx, username: member, *, message="*brak wiadomości*"):
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
    embed_msg.add_field(name="Serwer", value=client.get_guild(944920041361661952).name, inline=False)
    # embed_msg.add_field(name="Field3", value="Value3", inline=False)
    channel = await username.create_dm()

    await channel.send(embed=embed_msg)



@ping.error
async def ping_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR PING: {error}\n")
    if isinstance(error, MissingRequiredArgument):
        text = f"<@{user_error.id}>, spóbuj użyć: `!ping @NazwaUżytkownika`"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !ping ({msg_user})\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze! Sprawdź dokładniej :)"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} chciał dać pinga komuś kogo nie ma serwerze ({msg_user})")
    if isinstance(error, CommandOnCooldown):
        text = f"<@{user_error.id}>, spokojnie spokojnie, nie spiesz się tak z tym :D. Spróbuj ponownie za {error.retry_after:.2f}s"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} chciał za szybko użyć komendy !ping ({msg_user})")


@cooldown(1, 30, BucketType.user)
@client.command(name="komendy")
@has_permissions(send_messages=True)
async def komendy(ctx):
    reset_cooldown(ctx)
    user = ctx.message.author
    embed_msg = embed(title="Dostępne komendy na serwerze:",
                      description="`!zglos <propozycja/problem/bug` - jeśli chcesz coś zaproponować lub"
                                  " zgłosić problem/buga użyj tej komendy\n\n"
                                  "`!ping @NazwaUżytkownika` - umożliwa pingowanie użytownika "
                                  "(proszę nie nadużywać :))\n\n"
                                  "`!losowy-mem` - umożliwia wysłanie losowego mema ze strony memy.pl\n\n"
                                  "`!info` - możesz sprawdzić informacje o sobie lub o innych użytkownikach np."
                                  " !info @NazwaUżytkownika\n\n"
                                  "`...` - ...\n\n"
                                  "`...` - ...\n\n"
                                  "*kiedyś będzie ich więcej..*",
                      colour=discord.Colour.from_rgb(96, 223, 213))
    embed_msg.set_footer(text="komendy")
    embed_msg.timestamp = datetime.utcnow()
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(embed=embed_msg)
    logging.info(f"\n\nUżytkownik {user} użył komendy !komendy ({ctx.message.content})")


@komendy.error
async def komendy_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR KOMENDY: {error}\n")
    if isinstance(error, CommandOnCooldown):
        text = f"<@{user_error.id}>, ejj ty, czemu tak nadużywasz tej komendy? Poczekaj {error.retry_after:.2f}s i spróbuj ponownie."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} chciał za szybko użyć komendy !komendy ({msg_user})")


@client.command(name="lista")
@has_permissions(send_messages=True)
async def list_of_users(ctx):
    for guild in client.guilds:
        members = [f"{member.name}\n" for member in guild.members]
    embed_msg = embed(title="Lista wszystkich użytkowników:",
                      description="".join(members),
                      colour=discord.Colour.from_rgb(96, 223, 213))
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(embed=embed_msg)
    logging.info(f"\n\n{ctx.message.author.name} użył komendy !lista.\n\n")


@cooldown(1, 5, BucketType.user)
@client.command(name="losowy-mem")
@has_permissions(send_messages=True)
async def losowy_mem(ctx):
    reset_cooldown(ctx)
    username = ctx.message.author
    channel_mems = client.get_channel(int(1000405621444710460))
    print(channel_mems)
    if channel_mems.name == ctx.channel.name:
        await ctx.channel.purge(limit=1)
        mem = random_mem()
        msg = await channel_mems.send(mem)
        emojis = ["🤣", "🥱"]
        for emoji in emojis:
            await msg.add_reaction(emoji)
        logging.info(f"{username} wykorzystał komende !losowy-mem do losowego mema: {mem}")
    else:
        await ctx.channel.send(f"<@{username.id}>, używasz złego kanału. Przejdź na <#{channel_mems.id}>")
        logging.warning(f"{username} użył złego kanału do wysłania mema (#{ctx.channel.name})")


@losowy_mem.error
async def losowy_mem(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR LOSOWY-MEM: {error}\n")
    if isinstance(error, CommandOnCooldown):
        text = f"<@{user_error.id}>, poczekaj jeszcze chwilkę, dawka nowych memów już za: {error.retry_after:.2f}s."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} chciał za szybko użyć komendy !losoyw-mem ({msg_user})")


@client.command(name="info")
@has_permissions(send_messages=True)
async def info_about(ctx, *, username: discord.Member=" "):
    if not username == " ":
        username_created_at = username.created_at.strftime("%d-%m-%Y")
        username_name = username.display_name
        username_avatar = username.avatar_url
        username_joined_at = username.joined_at.strftime("%d-%m-%Y")
        username_status = str(username.status).title()

        members = sorted(ctx.guild.members, key=lambda member_join: member_join.joined_at)
        username_join_position = members.index(username)+1

        permission = [str(perm[0]).replace("_", " ").title() for perm in username.guild_permissions if perm[1]]
        permission_string = ", ".join(permission)

        embed_msg = embed(title="Informacje o koncie",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=username_name, icon_url=username_avatar)
        embed_msg.timestamp = datetime.utcnow()
        embed_msg.set_thumbnail(url=username_avatar)
        embed_msg.add_field(name="Status", value=username_status, inline=False)
        embed_msg.add_field(name="Pełna nazwa konta", value=username, inline=False)
        embed_msg.add_field(name="Data utworzenia konta", value=username_created_at, inline=False)
        # embed_msg.add_field(name="-", value="-", inline=False)
        embed_msg.add_field(name="Data dołączenia na serwer", value=username_joined_at, inline=False)
        embed_msg.add_field(name="Dołączył do sewera jako", value=username_join_position, inline=False)
        # embed_msg.add_field(name="-", value="-", inline=False)
        if len(username.roles) > 1:
            role_string = " ".join([role.mention for role in username.roles[1:]])
            embed_msg.add_field(name=f"Role [{len(username.roles)-1}]", value=role_string, inline=False)
        embed_msg.add_field(name=f"Uprawnienia [{len(permission)}]", value=permission_string, inline=False)
        embed_msg.set_footer(text=username.id)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed_msg)
        logging.info(f"{ctx.author.name} użył komendy !info.")
    else:
        username = ctx.author
        username_created_at = username.created_at.strftime("%d-%m-%Y")
        username_name = username.display_name
        username_avatar = username.avatar_url
        username_joined_at = username.joined_at.strftime("%d-%m-%Y")
        username_status = str(username.status).title()

        members = sorted(ctx.guild.members, key=lambda member_join: member_join.joined_at)
        username_join_position = members.index(username)+1

        permission = [str(perm[0]).replace("_", " ").title() for perm in username.guild_permissions if perm[1]]
        permission_string = ", ".join(permission)

        embed_msg = embed(title="Informacje o koncie",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=username_name, icon_url=username_avatar)
        embed_msg.timestamp = datetime.utcnow()
        embed_msg.set_thumbnail(url=username_avatar)
        embed_msg.add_field(name="Status", value=username_status, inline=False)
        embed_msg.add_field(name="Pełna nazwa konta", value=username, inline=False)
        embed_msg.add_field(name="Data utworzenia konta", value=username_created_at, inline=False)
        # embed_msg.add_field(name="-", value="-", inline=False)
        embed_msg.add_field(name="Data dołączenia na serwer", value=username_joined_at, inline=False)
        embed_msg.add_field(name="Dołączył do sewera jako", value=username_join_position, inline=False)
        # embed_msg.add_field(name="-", value="-", inline=False)
        if len(username.roles) > 1:
            role_string = " ".join([role.mention for role in username.roles[1:]])
            embed_msg.add_field(name=f"Role [{len(username.roles)-1}]", value=role_string, inline=False)
        embed_msg.add_field(name=f"Uprawnienia [{len(permission)}]", value=permission_string, inline=False)
        embed_msg.set_footer(text=username.id)
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(embed=embed_msg)
        logging.info(f"{username.name} użył komendy !info.")


@info_about.error
async def info_mem(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR INFO-ABOUT: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował użyć komendy !info do kogoś kogo nie ma na serwerze {msg_user}.\n")

# @client.event
# async def on_message(message):
#     if message.content == message.content:
#         emoji = "✅"
#         await message.add_reaction(emoji)

# @client.command(name="r")
# @has_permissions(administrator=True)
# async def r(ctx):
#     msg = ctx.message
#     print(msg.content)

client.run(client.get_token())
# file.close()
