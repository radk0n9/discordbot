# -*- coding: utf-8 -*-
import discord
import random
import sys
import datetime as dt
from my_client import MyClient

intents = discord.Intents.all()
client = MyClient(command_prefix="!", intents=intents, self_bot=False)
file = open("log.txt", "a", encoding="utf-8")
sys.stdout = file


def now_time():
    now = dt.datetime.now()
    date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
    return date_time


class SendMessage:
    def __init__(self, message):
        self.message = message

    def text_hi(self):
        if len(self.message.content) >= 3:
            with open("example_welcome.txt", "r", encoding="utf-8") as a:
                line_example_welcome = a.readlines()
                for line in line_example_welcome:
                    line_striped = line.strip()
                    if self.message.content == line_striped:
                        with open("welcome_txt.txt", "r", encoding="utf-8") as f:
                            lines_welcome_text = f.readlines()
                            choice_welcome_text = random.choice(lines_welcome_text)
                        return choice_welcome_text


class OnMember:
    def __init__(self, member):
        self.member = member

    def channel(self, channel):
        channel = str(channel)
        if channel == "witaj_i_zegnaj":
            channel = 991789338067210242
            return channel
        elif channel == "chat":
            channel = 944920042171170829
            return channel

    def when_member_join(self):
        member = self.member
        message = f"Witaj <@{member.id}>! Miło mi Ciebie gościć :)"
        print(f"{now_time()}: Użytkownik {member.name} dołączył do serwera.")
        return message

    def when_member_leave(self):
        member = self.member
        message = f"**{member.name}** właśnie nas opuścił/ła :("
        print(f"{now_time()}: Użytkownik {member.name} opuścił serwer.")
        return message

class OnMemberUpdate:
    def __init__(self, before, after):
        self.before = before
        self.after = after

    def when_member_boost_server(self):
        message = f"{self.after.mention} właśnie zboostował nasz serwer! Wielki dzięki za to :heart::partying_face:"
        print(f"{now_time()}: {self.after.name} właśnie zboostował serwer")
        return message

file.close()
