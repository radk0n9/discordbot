# TODO 1  twitch stream notification
# TODO 2 MEE6 check some new features
# TODO 3 Creating channel for someone
# TODO 6 Logging message edit

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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
intents.messages = True
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


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///messages-ranking.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)


# db.create_all()


def add_new_entry(id_user, username, value):
    new_user = Messages(id_user=id_user, username=username, value=value)
    db.session.add(new_user)
    db.session.commit()


@client.event
async def on_ready():
    channel = client.get_channel(999616411909496992)
    content = (await channel.history(limit=1).flatten())[0].embeds[0].fields[0].value
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
    bot = client.user

    # Informing when someone send direct message to bot
    if "Direct Message" in str(channel):
        channel_dm = client.get_channel(1002191158438539364)
        username = msg.author
        embed_msg = embed(title=f"Wiadomość od {username}",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.set_thumbnail(url=username.avatar_url)
        embed_msg.add_field(name="Treść", value=msg.content)
        embed_msg.set_footer(text=channel)
        embed_msg.timestamp = datetime.utcnow()
        await channel_dm.send(embed=embed_msg)
        logging.info(f"{channel} - prywatna wiadomość do {bot.name} o treści: <{msg.content}>")

    # Logging if statement for clearly logging information
    if "!" not in msg.content:
        if msg.content == "":
            logging.info(f"Użytkownik {msg.author} wysłał wiadomość <{msg.jump_url}> na kanale {channel}.")
        else:
            logging.info(f"Użytkownik {msg.author} wysłał wiadomość <{msg.content}> na kanale {channel}.")

    # Sending random message
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

    # Adding reactions for mem in mem channel
    if "https://" in msg.content or "http://" in msg.content or msg.attachments:
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
            if channel.name == "🔮・mems":
                emojis = ["🤣", "🥱"]
                for emoji in emojis:
                    await msg.add_reaction(emoji)
                logging.info(f"{msg.author.name} wysłał wiadomość: <{msg.content}> na kanale: {channel}.")

    # Database / Counting messages
    username_d = str(msg.author)
    try:
        id_query = Messages.query.filter_by(id_user=msg.author.id).first().id
        value_before = Messages.query.filter_by(id_user=msg.author.id).first().value
        new_value = int(value_before) + 1
        value_to_update = Messages.query.get(id_query)
        value_to_update.value = int(new_value)
        db.session.commit()
    except AttributeError:
        if msg.author.id != 945001935164030976:
            add_new_entry(msg.author.id, username_d, 1)
            logging.info(f"Dodano użytkownika <{username_d}> do bazdy danych wiadomości")

    await client.process_commands(msg)


@client.event
async def on_raw_message_delete(payload):
    try:
        msg_content = payload.cached_message.content
        channel = payload.cached_message.channel
        username = payload.cached_message.author
        logging.info(f"Użytkownik {username} usunął wiadomość: <{msg_content}> na kanale: {channel}")
    except AttributeError:
        pass


# @client.event
# async def on_raw_message_edit(payload):
#     msg_content = payload.cached_message.content
#     channel = payload.cached_message.channel
#     username = payload.cached_message.author
#     logging.info(f"Użytkownik {username} usunął wiadomość: {msg_content}; na kanale: {channel}")

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


client.run(DISCORD_TOKEN)
