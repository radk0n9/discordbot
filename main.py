# TODO 1  twitch stream notification
# TODO 2 MEE6 check some new features
# TODO 3 Creating channel for someone
# TODO 4 if someone write to bot send to channel
# TODO 5 Embed messages for !kick, !ban, !unban, !zglos

import discord
import requests
from datetime import datetime
import os
import random
from dotenv import load_dotenv
import logging
from logging import FileHandler, Formatter
from logging import INFO, NOTSET
from rich.logging import RichHandler
from discord.ext import commands


# Token section
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Logging section
rich_handler: RichHandler = RichHandler(rich_tracebacks=True)
rich_handler.setLevel(INFO)
rich_handler.setFormatter(Formatter("%(message)s"))
if not os.path.isdir('./Log'):
    os.makedirs('./Log', exist_ok=True)
file_handler = FileHandler(
    f"./Log/log{datetime.now():_%d-%m-%Y_%H-%M-%S-%f}.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    Formatter("%(asctime)s@ %(name)s [%(levelname)s] %(funcName)s: %(message)s"))
logging.basicConfig(level=NOTSET, handlers=[rich_handler, file_handler])

# Client discord setup
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents, self_bot=False)

embed = discord.Embed
user = discord.User
message = discord.Message
member = discord.Member

# Cogs importing
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension("cogs." + cog[:-3])


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


@client.event
async def on_ready():
    channel = client.get_channel(999616411909496992)
    content = (await channel.history(limit=1).flatten())[0].embeds[0].description
    if content == "*Aktywny* :green_circle:":
        activity = discord.Game(name="Jest problem? !zglos")
        status_bot = discord.Status.online
        await client.change_presence(status=status_bot, activity=activity)
        logging.info(f"Ustawiono status bota na: Aktywny.")
    if content == "*Prace techniczne* :yellow_circle:":
        activity = discord.Game(name="RaDkon mnie naprawia :)))")
        status_bot = discord.Status.idle
        await client.change_presence(status=status_bot, activity=activity)
        logging.info(f"Ustawiono status bota na: Prace techniczne.")
    if content == "*Przerwa*: :no_entry:":
        activity = discord.Game(name="Mała przerwa..")
        status_bot = discord.Status.do_not_disturb
        await client.change_presence(status=status_bot, activity=activity)
        logging.info(f"Ustawiono status bota na: Przerwa.")
    logging.info(f"Discord bot working...")


@client.event
async def on_message(msg):
    channel = msg.channel
    logging.info(f"{msg.author.name} wysłał wiadomość {msg.content}; na kanale {channel}.")
    if len(msg.content) >= 3:
        if channel.id == 944920042171170829:
            with open("example_welcome.txt", "r", encoding="utf-8") as a:
                line_example_welcome = a.readlines()
                for line in line_example_welcome:
                    line_striped = line.strip()
                    if msg.content == line_striped:
                        with open("welcome_txt.txt", "r", encoding="utf-8") as f:
                            lines_welcome_text = f.readlines()
                            choice_welcome_text = random.choice(lines_welcome_text)
                        try:
                            await msg.channel.send(choice_welcome_text)
                        except discord.errors.HTTPException:
                            pass

    if "https://" in msg.content or "http://" in msg.content or msg.attachments:
        print("hej")
        try:
            message_attachments = msg.attachments[0]
            filename = message_attachments.filename
            url = message_attachments.url
            if channel.name == "🔮・mems":
                emojis = ["🤣", "🥱"]
                for emoji in emojis:
                    await msg.add_reaction(emoji)

                logging.info(f"Dodano reakcje: {emojis} do wiadomości {msg.author.name} o treści <{msg.content},"
                             f" nazwa pliki: {filename}, link do pliku: {url}> na kanale: {channel}")
        except IndexError:
            emojis = ["🤣", "🥱"]
            for emoji in emojis:
                await msg.add_reaction(emoji)
            logging.info(f"{msg.author.name} wysłał wiadomość: <{msg.content}> na kanale: {channel}.")

    await client.process_commands(msg)


@client.event
async def on_member_join(member_guild):
    channel = client.get_channel(991789338067210242)
    msg = f"Witaj <@{member_guild.id}>! Miło mi Ciebie gościć :)"
    logging.info(f"Użytkownik {member.name} dołączył do serwera.")
    await channel.send(msg)


@client.event
async def on_member_remove(member_guild):
    channel = client.get_channel(991789338067210242)
    msg = f"**{member_guild.name}** właśnie nas opuścił/ła :("
    logging.info(f"Użytkownik {member_guild.name} opuścił serwer.")
    await channel.send(msg)


@client.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        new_role = next(role for role in after.roles if role not in before.roles)
        channel = client.get_channel(944920042171170829)
        if new_role.name == "Server Booster":
            msg = f"{after.mention} właśnie zboostował nasz serwer! Wielki dzięki za to :heart::partying_face:"
            logging.info(f"{after.name} właśnie zboostował serwer.")
            await channel.send(msg)


# @client.event
# async def on_raw_reaction_add(payload):
#     message_regulamin = 999688170927042643
#     message_plec = 996145295014502410
#     message_wiek = 996147074322153513
#     message_gry = 996149490119618580
#     message_przeczytaj_to = 996854970764754954
#     guild = client.get_guild(payload.guild_id)
#     # member = guild.get_member(payload.user_id)
#
#     if payload.message_id == message_regulamin:
#         role = discord.utils.get(guild.roles, name="☑️")
#         await payload.member.add_roles(role)
#         logging.info(f"Dodano role {role} - {payload.member.name}.")
#
#     if payload.message_id == message_przeczytaj_to:
#         role = discord.utils.get(guild.roles, name="Beta-Tester")
#         await payload.member.add_roles(role)
#         logging.info(f"Dodano role {role} - {payload.member.name}.")
#
#     if payload.message_id == message_plec:
#         for rola in ROLE_DICT_PLEC:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
#                 await payload.member.add_roles(role)
#                 logging.info(f"Dodano role {role} - {payload.member.name}.")
#
#     if payload.message_id == message_wiek:
#         for rola in ROLE_DICT_WIEK:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
#                 await payload.member.add_roles(role)
#                 logging.info(f"Dodano role {role} - {payload.member.name}.")
#
#     if payload.message_id == message_gry:
#         for rola in ROLE_DICT_GRY:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
#                 await payload.member.add_roles(role)
#                 logging.info(f"Dodano role {role} - {payload.member.name}.")
#
#
# @client.event
# async def on_raw_reaction_remove(payload):
#     message_regulamin = 999688170927042643
#     message_plec = 996145295014502410
#     message_wiek = 996147074322153513
#     message_gry = 996149490119618580
#     message_przeczytaj_to = 996854970764754954
#     guild = client.get_guild(payload.guild_id)
#     member = guild.get_member(payload.user_id)
#
#     if payload.message_id == message_regulamin:
#         role = discord.utils.get(guild.roles, name="☑️")
#         await member.remove_roles(role)
#         logging.info(f"Usunieto role {role} - {member.name}.")
#
#     if payload.message_id == message_przeczytaj_to:
#         role = discord.utils.get(guild.roles, name="Beta-Tester")
#         await member.remove_roles(role)
#         logging.info(f"Usunieto role {role} - {member.name}.")
#
#     if payload.message_id == message_plec:
#         for rola in ROLE_DICT_PLEC:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
#                 await member.remove_roles(role)
#                 logging.info(f"Usunieto role {role} - {member.name}.")
#
#     if payload.message_id == message_wiek:
#         for rola in ROLE_DICT_WIEK:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
#                 await member.remove_roles(role)
#                 logging.info(f"Usunieto role {role} - {member.name}.")
#
#     if payload.message_id == message_gry:
#         for rola in ROLE_DICT_GRY:
#             if payload.emoji.name == rola:
#                 role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
#                 await member.remove_roles(role)
#                 logging.info(f"Usunieto role {role} - {member.name}.")

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

client.run(DISCORD_TOKEN)
# file.close()
