# -*- coding: utf-8 -*-
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
from discord.ext.commands import has_permissions, MissingPermissions, MemberNotFound, MissingRequiredArgument

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
    date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
    return date_time


intents = discord.Intents.all()
intents.members = True
client = MyClient(command_prefix="!", intents=intents, self_bot=False)


embed = discord.Embed
user = discord.User
message = discord.Message
member = discord.Member

client.clearing()
client.list_users()
client.report_a_problem()


@client.event
async def on_message(msg):
    channel = msg.channel
    print(f"{now_time()}: {msg.author.name} wysłał wiadomość: <{msg.content}> na kanale: {channel}")
    send_message = SendMessage(msg)
    content = send_message.text_hi()
    try:
        await msg.channel.send(content)
    except discord.errors.HTTPException:
        pass
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


# @client.event
# async def on_message(msg):
#     channel = msg.channel
#     print(f"{now_time()}: {msg.author.name} wysłał wiadomość: <{msg.content}> na kanale: {channel}")
#     await client.process_commands(msg)

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
    message_regulamin = 996167907375595610
    message_plec = 996145295014502410
    message_wiek = 996147074322153513
    message_gry = 996149490119618580
    message_przeczytaj_to = 996854970764754954
    guild = client.get_guild(payload.guild_id)
    # member = guild.get_member(payload.user_id)

    if payload.message_id == message_regulamin:
        role = discord.utils.get(guild.roles, name="☑️")
        await payload.member.add_roles(role)
        print(f"{now_time()}: Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await payload.member.add_roles(role)
        print(f"{now_time()}: Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await payload.member.add_roles(role)
                print(f"{now_time()}: Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await payload.member.add_roles(role)
                print(f"{now_time()}: Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await payload.member.add_roles(role)
                print(f"{now_time()}: Dodano role {role} - {payload.member.name}")


@client.event
async def on_raw_reaction_remove(payload):
    message_regulamin = 996167907375595610
    message_plec = 996145295014502410
    message_wiek = 996147074322153513
    message_gry = 996149490119618580
    message_przeczytaj_to = 996854970764754954
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.message_id == message_regulamin:
        role = discord.utils.get(guild.roles, name="☑️")
        await member.remove_roles(role)
        print(f"{now_time()}: Usunieto role {role} - {member.name}")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await member.remove_roles(role)
        print(f"{now_time()}: Usunieto role {role} - {member.name}")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await member.remove_roles(role)
                print(f"{now_time()}: Usunieto role {role} - {member.name}")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await member.remove_roles(role)
                print(f"{now_time()}: Usunieto role {role} - {member.name}")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await member.remove_roles(role)
                print(f"{now_time()}: Usunieto role {role} - {member.name}")


@client.command(name="kick")
@has_permissions(kick_members=True)
async def kick(ctx, username: member, *, reason):
    print(f"{now_time()}: {ctx.message.author.name} wyrzucił {username.display_name} za: {reason}")
    await ctx.channel.purge(limit=1)
    await username.kick(reason=reason)
    await ctx.channel.send(f"<@{ctx.message.author.id}> wyrzucił {username.display_name} za: **{reason}**.")


@kick.error
async def kick_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    print(f"\nERROR KICK: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował wyrzucić kogoś kogo nie ma na serwerze.")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!kick <ID użytkownika> <powód>`'
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} źle użył komendy !kick ({msg_user}).")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował kogoś wyrzuć za pomocą komendy !kick ({msg_user}).")


@client.command(name="ban")
@has_permissions(ban_members=True)
async def ban(ctx, username: member, *, reason, delete_message_days=7):
    print(f"{now_time()}: {ctx.message.author.name} zbanował {username.display_name} za: {reason}, "
          f"usunięto wiadomości z {delete_message_days} dni.")
    await ctx.channel.purge(limit=1)
    await username.ban(reason=reason, delete_message_days=delete_message_days)
    await ctx.channel.send(f"<@{ctx.message.author.id}> zbanował {username.display_name} za: **{reason}**, "
                           f"usunięto wiadomości z **{delete_message_days}** dni.")


@ban.error
async def ban_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    print(f"\nERROR BAN: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował zbanować kogoś kogo nie ma na serwerze.")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!ban <ID użytkownika> <powód>' \
               f' <z ilu dni usunąć wiadomości, zakres od 0 do 7>`'
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} źle użył komendy !ban ({msg_user}).")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował kogoś zbanować za pomocą komendy !ban ({msg_user}).")


@client.command(name="unban")
@has_permissions(ban_members=True)
async def unban(ctx, username: discord.User, *, reason):
    print(f"{now_time()}: {ctx.message.author.name} odbanował {username.display_name} z powodu: {reason}")
    await ctx.channel.purge(limit=1)
    await ctx.guild.unban(username, reason=reason)
    await ctx.channel.send(f"<@{ctx.message.author.id}> odbanował {username.display_name} za: **{reason}**")


@unban.error
async def unban_error(ctx, error):
    user_error = ctx.message.author
    msg_user = ctx.message.content
    print(f"\nERROR UNBAN: {error}\n")
    if isinstance(error, MemberNotFound):
        text = f"<@{user_error.id}>, nie ma takiego użytkownika na serwerze."
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował odbanować kogoś kogo nie ma na serwerze.")
    if isinstance(error, MissingRequiredArgument):
        text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!unban <ID użytkownika> <powód>'
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} źle użył komendy !unban ({msg_user}).")
    if isinstance(error, MissingPermissions):
        text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
        await ctx.channel.send(text)
        print(f"{now_time()}: Użytkownik {user_error} próbwował kogoś odbanować za pomocą komendy !unban ({msg_user}).")


# @client.event
# async def on_message(message):
#     if message.content == message.content:
#         emoji = "♿"
#         await message.add_reaction(emoji)

# @client.command(name="r")
# @has_permissions(administrator=True)
# async def r(ctx):
#     msg = ctx.message
#     print(msg.content)

client.run(client.get_token())
# file.close()
