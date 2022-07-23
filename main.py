# -*- coding: utf-8 -*-
# TODO Memes random sender, twitch stream notification

import discord
import sys
from datetime import datetime
import os
import logging
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET
from rich.logging import RichHandler
from my_client import MyClient
from event import SendMessage, OnMember, OnMemberUpdate
from role_dict import ROLE_DICT_PLEC, ROLE_DICT_WIEK, ROLE_DICT_GRY
from discord.ext.commands import has_permissions, MissingPermissions, MemberNotFound, MissingRequiredArgument, cooldown,\
    BucketType, CommandOnCooldown

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


def now_time():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return date_time


intents = discord.Intents.all()
intents.members = True
client = MyClient(command_prefix="!", intents=intents, self_bot=False)


embed = discord.Embed
user = discord.User
message = discord.Message
member = discord.Member

client.clearing()
client.report_a_problem()


def reset_cooldown(ctx):
    if ctx.message.author.id == 287292834355347456:
        return ctx.command.reset_cooldown(ctx)

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
                emojis = ("🤣", "🥱")
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


@client.command(name="plec")
@has_permissions(administrator=True)
async def plec(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    embed_msg = embed(title="Wybierz swoją płeć:",
                      description="\n"
                                  ":man_gesturing_no: : Mężczyzna\n"
                                  "\n"
                                  ":person_gesturing_no: : Kobieta\n",
                      colour=discord.Colour.dark_magenta(),
                      )
    msg = await ctx.channel.send(embed=embed_msg)
    emojis = ROLE_DICT_PLEC
    for emoji in emojis:
        await msg.add_reaction(emoji)


@client.command(name="wiek")
@has_permissions(administrator=True)
async def wiek(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    embed_msg = embed(title="Wybierz swój wiek:",
                      description="\n"
                                  "👶 : 12+\n"
                                  "\n"
                                  "🧒 : 14+\n"
                                  "\n"
                                  "👦 : 16+\n"
                                  "\n"
                                  "🧑 : 18+\n"
                                  "\n"
                                  "‍️👨‍🦰 : 20+\n"
                                  "\n"
                                  "🧔‍♂️ : 22+\n"
                                  "\n"
                                  "👴 : 24+\n",

                      colour=discord.Colour.dark_purple(),
                      )
    msg = await ctx.channel.send(embed=embed_msg)
    emojis = ROLE_DICT_WIEK
    for emoji in emojis:
        await msg.add_reaction(emoji)


@client.command(name="gry")
@has_permissions(administrator=True)
async def gry(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    embed_msg = embed(title="Wybierz gry, w ktore grasz:",
                      description="\n"
                                  "👨‍👩‍👧  : Among Us\n"     
                                  "\n"
                                  "🔫 : Counter-Strike: Global Offensive\n"
                                  "\n"
                                  "🚚 : Euro Truck Simulator 2\n"
                                  "\n"
                                  "🪅 : Fortnite\n"
                                  "\n"
                                  "🚙 : Forza Horizon 4\n"
                                  "\n"
                                  "🚗 : Forza Horizon 5\n"  
                                  "\n"
                                  "‍️💵 : Grand Theft Auto V\n"
                                  "\n"
                                  ":regional_indicator_l: : League of Legends\n"
                                  "\n"
                                  "⚒ ️: Minecraft\n"
                                  "\n"
                                  "6️⃣ : Tom Clancy's Rainbow Six Siege\n"
                                  "\n"
                                  ":regional_indicator_v: : Valorant\n",
                      colour=discord.Colour.dark_green(),
                      )
    msg = await ctx.channel.send(embed=embed_msg)
    emojis = ROLE_DICT_GRY
    for emoji in emojis:
        await msg.add_reaction(emoji)


@client.event
async def on_raw_reaction_add(payload):
    message_regulamin = 999688170927042643
    message_plec = 996145295014502410
    message_wiek = 996147074322153513
    message_gry = 996149490119618580
    message_przeczytaj_to = 996854970764754954
    guild = client.get_guild(payload.guild_id)
    # member = guild.get_member(payload.user_id)

    if payload.message_id == message_regulamin:
        role = discord.utils.get(guild.roles, name="☑️")
        await payload.member.add_roles(role)
        logging.info(f"\n\nDodano role {role} - {payload.member.name}.\n")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await payload.member.add_roles(role)
        logging.info(f"\n\nDodano role {role} - {payload.member.name}.\n")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await payload.member.add_roles(role)
                logging.info(f"\n\nDodano role {role} - {payload.member.name}.\n")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await payload.member.add_roles(role)
                logging.info(f"\n\nDodano role {role} - {payload.member.name}.\n")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await payload.member.add_roles(role)
                logging.info(f"\n\nDodano role {role} - {payload.member.name}.\n")


@client.event
async def on_raw_reaction_remove(payload):
    message_regulamin = 999688170927042643
    message_plec = 996145295014502410
    message_wiek = 996147074322153513
    message_gry = 996149490119618580
    message_przeczytaj_to = 996854970764754954
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.message_id == message_regulamin:
        role = discord.utils.get(guild.roles, name="☑️")
        await member.remove_roles(role)
        logging.info(f"\n\nUsunieto role {role} - {member.name}.\n")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await member.remove_roles(role)
        logging.info(f"\n\nUsunieto role {role} - {member.name}.\n")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await member.remove_roles(role)
                logging.info(f"\n\nUsunieto role {role} - {member.name}.\n")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await member.remove_roles(role)
                logging.info(f"\n\nUsunieto role {role} - {member.name}.\n")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await member.remove_roles(role)
                logging.info(f"\n\nUsunieto role {role} - {member.name}.\n")


@client.command(name="kick")
@has_permissions(kick_members=True)
async def kick(ctx, username: member, *, reason):
    logging.warning(f"\n\n{ctx.message.author.name} wyrzucił {username.display_name} za: {reason}.\n")
    await ctx.channel.purge(limit=1)
    await username.kick(reason=reason)
    await ctx.channel.send(f"<@{ctx.message.author.id}> wyrzucił {username.display_name} za: **{reason}**.")


@kick.error
async def kick_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR KICK: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował wyrzucić kogoś kogo nie ma na serwerze.\n")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!kick <ID użytkownika> <powód>`'
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !kick ({msg_user}).\n")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował kogoś wyrzuć za pomocą komendy !kick ({msg_user}).\n")


@client.command(name="ban")
@has_permissions(ban_members=True)
async def ban(ctx, username: member, *, reason, delete_message_days=7):
    logging.warning(f"\n\n{ctx.message.author.name} zbanował {username.display_name} za: {reason}, "
          f"usunięto wiadomości z {delete_message_days} dni.\n")
    await ctx.channel.purge(limit=1)
    await username.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.channel.send(f"<@{ctx.message.author.id}> zbanował {username.display_name} za: **{reason}**, "
                           f"usunięto wiadomości z **{delete_message_days}** dni.")


@ban.error
async def ban_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR BAN: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował zbanować kogoś kogo nie ma na serwerze.\n")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!ban <ID użytkownika> <powód>' \
               f' <z ilu dni usunąć wiadomości, zakres od 0 do 7>`'
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !ban ({msg_user}).\n")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował kogoś zbanować za pomocą komendy !ban ({msg_user}).\n")


@client.command(name="unban")
@has_permissions(ban_members=True)
async def unban(ctx, username: discord.User, *, reason):
    logging.warning(f"\n\n{ctx.message.author.name} odbanował {username.display_name} z powodu: {reason}.\n")
    await ctx.channel.purge(limit=1)
    await ctx.guild.unban(username, reason=reason)
    await ctx.channel.send(f"<@{ctx.message.author.id}> odbanował {username.display_name} za: **{reason}**.")


@unban.error
async def unban_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    logging.error(f"\n\nERROR UNBAN: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował odbanować kogoś kogo nie ma na serwerze.\n")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!unban <ID użytkownika> <powód>'
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !unban ({msg_user}).\n")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        logging.error(f"\n\nUżytkownik {user_error} próbwował kogoś odbanować za pomocą komendy !unban ({msg_user}).\n")


@cooldown(1, 30, BucketType.user)
@client.command(name="ping")
@has_permissions(send_messages=True)
async def ping(ctx, username: member):
    reset_cooldown(ctx)
    pinger = ctx.message.author
    channel = await username.create_dm()
    await ctx.channel.purge(limit=1)
    await channel.send(f"*PING* -> Dostałeś **PING'a** od użytkownika **{pinger.name}**! <- *PING* // "
                       f"Serwer: **{client.get_guild(944920041361661952).name}**")


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
                                  "`...` - ...\n\n"
                                  "`...` - ...\n\n"
                                  "*kiedyś będzie ich więcej..*",
                      colour=discord.Colour.from_rgb(96, 223, 213))
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


@client.command(name="status")
@has_permissions(administrator=True)
async def status(ctx, param):
    if param == "aktywny":
        activity = discord.Game(name="Jest problem? !zglos")
        status_bot = discord.Status.online
        await client.change_presence(status=status_bot, activity=activity)
        embed_msg = embed(title="Status bota:",
                          description="*Aktywny* :green_circle:",
                          colour=discord.Colour.green())
        await ctx.channel.purge(limit=2)
        await ctx.channel.send(embed=embed_msg)
        logging.info(f"\n\nUstawiono status bota na: Aktywny.\n\n")
    if param == "prace-techniczne":
        activity = discord.Game(name="RaDkon mnie naprawia :)))")
        status_bot = discord.Status.idle
        await client.change_presence(status=status_bot, activity=activity)
        embed_msg = embed(title="Status bota:",
                          description="*Prace techniczne* :yellow_circle:",
                          colour=discord.Colour.from_rgb(255, 255, 0))
        await ctx.channel.purge(limit=2)
        await ctx.channel.send(embed=embed_msg)
        logging.info(f"\n\nUstawiono status bota na: Prace techniczne.\n\n")
    if param == "przerwa":
        activity = discord.Game(name="Mała przerwa..")
        status_bot = discord.Status.do_not_disturb
        await client.change_presence(status=status_bot, activity=activity)
        embed_msg = embed(title="Status bota:",
                          description="*Przerwa*: :no_entry:",
                          colour=discord.Colour.from_rgb(255, 0, 0))
        await ctx.channel.purge(limit=2)
        await ctx.channel.send(embed=embed_msg)
        logging.info(f"\n\nUstawiono status bota na: Przerwa.\n\n")

        #
    # logging.info(f"\n\n{ctx.message.author.name} użył komendy !lista.\n\n")

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
