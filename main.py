# TODO 1  twitch stream notification
# TODO 2 MEE6 check some new features
# TODO 3 Creating channel for someone
# TODO 4 Automod spam!
# TODO 5 Change on_remove event when someone was kicked
import time

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

# embed = discord.Embed
# user = discord.User
# message = discord.Message
# member = discord.Member

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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///discord-bot-database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)


class OwnerMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, unique=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)


db.create_all()


def add_new_entry(id_user, value):
    new_user = Messages(id_user=id_user, value=value)
    db.session.add(new_user)
    db.session.commit()


def add_new_entry_owner(id_user, value):
    new_user = OwnerMessages(id_user=id_user, value=value)
    db.session.add(new_user)
    db.session.commit()


def adding_value(what, message_author_id, t=None):
    if what == "owner_messages":
        t = OwnerMessages
    if what == "messages":
        t = Messages
    id_query = t.query.filter_by(id_user=message_author_id).first().id
    value_before = t.query.filter_by(id_user=message_author_id).first().value
    new_value = int(value_before) + 1
    value_to_update = t.query.get(id_query)
    value_to_update.value = int(new_value)
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
async def on_message(message):
    channel = message.channel
    bot = client.user

    # Informing when someone send direct message to bot
    if "Direct Message" in str(channel):
        channel_dm = client.get_channel(1002191158438539364)
        username = message.author
        embed_msg = embed(title=f"Wiadomość od {username}",
                          description="",
                          colour=discord.Colour.random())
        embed_msg.set_author(name=bot.display_name, icon_url=bot.avatar_url)
        embed_msg.set_thumbnail(url=username.avatar_url)
        embed_msg.add_field(name="Treść", value=message.content)
        embed_msg.set_footer(text=channel)
        embed_msg.timestamp = datetime.utcnow()
        await channel_dm.send(embed=embed_msg)
        logging.info(f"{channel} - prywatna wiadomość do {bot.name} o treści: <{message.content}>")

    # Logging if statement for clearly logging information
    if "!" not in message.content:
        if message.content == "":
            logging.info(f"Użytkownik {message.author} wysłał wiadomość <{message.jump_url}> na kanale {channel}.")
        else:
            logging.info(f"Użytkownik {message.author} wysłał wiadomość <{message.content}> na kanale {channel}.")

    # Sending random message
    if len(message.content) >= 3:
        if channel.id == 944920042171170829:
            with open("example_welcome.txt", "r", encoding="utf-8") as a:
                line_example_welcome = a.readlines()
                for line in line_example_welcome:
                    line_striped = line.strip()
                    if message.content == line_striped:
                        with open("welcome_txt.txt", "r", encoding="utf-8") as f:
                            lines_welcome_text = f.readlines()
                            choice_welcome_text = random.choice(lines_welcome_text)
                        try:
                            await message.channel.send(choice_welcome_text)
                        except discord.errors.HTTPException:
                            pass

    # Adding reactions for mem in mem channel
    if "https://" in message.content or "http://" in message.content or message.attachments:
        try:
            message_attachments = message.attachments[0]
            filename = message_attachments.filename
            url = message_attachments.url
            if channel.name == "🔮・mems":
                emojis = ["🤣", "🥱"]
                for emoji in emojis:
                    await message.add_reaction(emoji)

                logging.info(
                    f"Dodano reakcje: {emojis} do wiadomości {message.author.name} o treści <{message.content},"
                    f" nazwa pliki: {filename}, link do pliku: {url}> na kanale: {channel}")
        except IndexError:
            if channel.name == "🔮・mems":
                emojis = ["🤣", "🥱"]
                for emoji in emojis:
                    await message.add_reaction(emoji)
                logging.info(f"{message.author.name} wysłał wiadomość: <{message.content}> na kanale: {channel}.")

    # Database / Counting messages
    username_d = str(message.author)

    if message.author.id == 945001935164030976 or message.author.id == 287292834355347456:
        try:
            adding_value("owner_messages", message.author.id)
        except AttributeError:
            add_new_entry_owner(message.author.id, 1)
            logging.info(f"Dodano użytkownika <{username_d}> do bazdy danych wiadomości <OwnerMessage>")
    else:
        try:
            adding_value("messages", message.author.id)
        except AttributeError:
            add_new_entry(message.author.id, 1)
            logging.info(f"Dodano użytkownika <{username_d}> do bazdy danych wiadomości <Messages>")

    await client.process_commands(message)


@client.event
async def on_raw_message_delete(payload):
    try:
        msg_content = payload.cached_message.content
        channel = payload.cached_message.channel
        username = payload.cached_message.author
        logging.info(f"Użytkownik {username} usunął wiadomość: <{msg_content}> na kanale: {channel}")
    except AttributeError:
        pass


@client.event
async def on_raw_message_edit(payload):
    try:
        before_message = payload.cached_message.content
        channel = payload.cached_message.channel
        username = payload.cached_message.author
        after_message = payload.data["content"]
        logging.info(f"Użytkownik {username} edytował wiadomość <{before_message}> na wiadomość <{after_message}>"
                     f" na kanale: {channel}")
    except KeyError:
        pass


@client.event
async def on_member_join(member):
    channel = client.get_channel(991789338067210242)
    msg = f"Witaj <@{member.id}>! Miło mi Ciebie gościć :)"
    logging.info(f"Użytkownik {member.name} dołączył do serwera.")
    await channel.send(msg)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(991789338067210242)
    msg = f"**{member.name}** właśnie nas opuścił/ła :("
    logging.info(f"Użytkownik {member.name} opuścił serwer.")
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


@client.event
async def on_voice_state_update(member, before, after):
    guild_server_id = member.guild.id
    guild = client.get_guild(int(guild_server_id))
    global own_channel_user
    if not before.channel and after.channel.id == 1002508594304000121:
        cat = client.get_channel(1002538949463515196)
        username_channel = str(member)
        logging.info(f"<{member}> stworzył swój kanał przy pomocy kanału <{after.channel.name}>")
        own_channel_user = await guild.create_voice_channel(name=username_channel, category=cat,
                                                            topic=f"Kanał użytkownik {username_channel}")
        logging.info(f"Przeniesiono użytkownika <{member}> na kanał <{own_channel_user.name}>")
        await member.move_to(own_channel_user)

    if before.channel and not after.channel:
        if before.channel.id == own_channel_user.id:
            logging.info(f"Użytkownik <{member}> opuścił kanał <{own_channel_user.name}>, usunięto kanał")
            await own_channel_user.delete()



client.run(DISCORD_TOKEN)
