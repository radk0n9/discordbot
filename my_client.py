# -*- coding: utf-8 -*-
import time
import sys
import discord
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument

# file = open("log.txt", "a", encoding="utf-8")
# sys.stdout = file
# intents = discord.Intents.all()
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def now_time():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return date_time


class MyClient(commands.Bot):
    def __int__(self, command_prefix, intents, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.clearing()
        self.list_users()
        self.report_a_problem()

    async def on_ready(self):
        activity = discord.Game(name="Jest problem? !zglos")
        await self.change_presence(activity=activity)
        logging.info(f"\n\nDiscord bot working...\n")

    def get_token(self):
        return DISCORD_TOKEN

    def clearing(self):
        @self.command(name="clear")
        @has_permissions(administrator=True)
        async def clear(ctx, amount=2):
            user = ctx.message.author.name
            messages_deleted = await ctx.channel.purge(limit=amount)
            total_deleted = len(messages_deleted)
            logging.info(f"\n\nUsuwanie {total_deleted} wiadomości przez {user}.\n")


        @clear.error
        async def clear_error(ctx, error):
            user_error = ctx.message.author
            if isinstance(error, MissingPermissions):
                text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
                await ctx.channel.send(text)
                logging.warning(f"\n\nUżytkownik {user_error} próbwował usunąć wiadomości.\n")

        @self.command(name="clear-all")
        @has_permissions(administrator=True)
        async def clear_all(ctx):
            user = ctx.message.author.name
            messages_deleted = await ctx.channel.purge()
            total_deleted = len(messages_deleted)
            logging.info(f"\n\nUsuwanie {total_deleted} wiadomości przez {user}.\n\n")

        @clear_all.error
        async def clear_all_error(ctx, error):
            user_error = ctx.message.author
            if isinstance(error, MissingPermissions):
                msg = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
                await ctx.channel.send(msg)
                logging.warning(f"\n\nUżytkownik {user_error} próbwował usunąć wszystkie wiadomości.\n\n")

    def list_users(self):
        @self.command(name="lista")
        async def list_of_users(ctx):
            for guild in self.guilds:
                members = [f"`{member.name}`\n" for member in guild.members]
            message1 = f"Lista wszystkich użytkowników:\n"
            message2 = "".join(members)
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(message1 + message2)
            logging.warning(f"\n\n{ctx.message.author.name} użył komendy !list-users.\n\n")

    def report_a_problem(self):
        @self.command(name="zglos")
        async def report_a_problem(ctx, *, problem):
            channel_problemy = self.get_channel(996485249989103616)
            channel = ctx.channel.id
            member = ctx.message.author
            await ctx.channel.purge(limit=1)
            await ctx.send(f'<@{member.id}>, dziękuję za zgłoszenie o treści: `{problem}`')
            await channel_problemy.send(f"**Problem/Bug/Propozycja:**\n"
                                        f"\n{problem}\n"
                                        f"\nZgłoszone przez <@{member.id}>")
            logging.error(f'\n\nUżytkownik {member} zgłosił buga/problem/propozycję o treści: "{problem}".\n')

        @report_a_problem.error
        async def report_a_problem_error(ctx, error):
            user_error = ctx.message.author
            if isinstance(error, MissingRequiredArgument):
                msg = f'<@{user_error.id}>, aby zgłosić buga/problem/propozycje napisz:' \
                      f'\n`!zglos <treść buga/problemu/propozycji>`'
                await ctx.channel.send(msg)
                logging.warning(f'\n\nUżytkownik {user_error} źle użył komendy !zglos "{ctx.message.content}".\n')


# file.close()
