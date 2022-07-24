import time
import sys
import discord
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, MemberNotFound, MissingRequiredArgument, cooldown,\
    BucketType, CommandOnCooldown
from role_dict import ROLE_DICT_PLEC, ROLE_DICT_WIEK, ROLE_DICT_GRY


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

embed = discord.Embed
user = discord.User
message = discord.Message
member = discord.Member


def now_time():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return date_time


def reset_cooldown(ctx):
    if ctx.message.author.id == 287292834355347456:
        return ctx.command.reset_cooldown(ctx)


class MyClient(commands.Bot):
    def __int__(self, command_prefix, intents, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.clearing()
        self.report_a_problem()

    async def on_ready(self):
        channel = self.get_channel(999616411909496992)
        content = (await channel.history(limit=1).flatten())[0].embeds[0].description
        if content == "*Aktywny* :green_circle:":
            activity = discord.Game(name="Jest problem? !zglos")
            status_bot = discord.Status.online
            await self.change_presence(status=status_bot, activity=activity)
            logging.info(f"\n\nUstawiono status bota na: Aktywny.\n\n")
        if content == "*Prace techniczne* :yellow_circle:":
            activity = discord.Game(name="RaDkon mnie naprawia :)))")
            status_bot = discord.Status.idle
            await self.change_presence(status=status_bot, activity=activity)
            logging.info(f"\n\nUstawiono status bota na: Prace techniczne.\n\n")
        if content == "*Przerwa*: :no_entry:":
            activity = discord.Game(name="Mała przerwa..")
            status_bot = discord.Status.do_not_disturb
            await self.change_presence(status=status_bot, activity=activity)
            logging.info(f"\n\nUstawiono status bota na: Przerwa.\n\n")
        logging.info(f"\n\nDiscord bot working...\n")

    def get_token(self):
        return DISCORD_TOKEN

    def clearing(self):
        @self.command(name="clear")
        @has_permissions(administrator=True)
        async def clear(ctx, amount=2):
            user = ctx.message.author.name
            await ctx.channel.purge(limit=1)
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

    def report_a_problem(self):
        @self.command(name="zglos")
        async def report_a_problem(ctx, *, problem):
            channel_problemy = self.get_channel(996485249989103616)
            channel = ctx.channel.id
            member = ctx.message.author
            await ctx.channel.purge(limit=1)
            msg = await ctx.send(f'<@{member.id}>, dziękuję za zgłoszenie o treści: `{problem}`')
            emojis = ["👍🏼", "👎🏼"]
            for emoji in emojis:
                await msg.add_reaction(emoji=emoji)
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

    def status_of_bot(self):
        @self.command(name="status")
        @has_permissions(administrator=True)
        async def status(ctx, param):
            if param == "aktywny":
                activity = discord.Game(name="Jest problem? !zglos")
                status_bot = discord.Status.online
                await self.change_presence(status=status_bot, activity=activity)
                embed_msg = embed(title="Status bota:",
                                  description="*Aktywny* :green_circle:",
                                  colour=discord.Colour.green())
                embed_msg.timestamp = datetime.utcnow()
                embed_msg.set_footer(text="RaDkon")
                await ctx.channel.purge(limit=2)
                await ctx.channel.send(embed=embed_msg)
                logging.info(f"\n\nUstawiono status bota na: Aktywny.\n\n")
            if param == "prace-techniczne":
                activity = discord.Game(name="RaDkon mnie naprawia :)))")
                status_bot = discord.Status.idle
                await self.change_presence(status=status_bot, activity=activity)
                embed_msg = embed(title="Status bota:",
                                  description="*Prace techniczne* :yellow_circle:",
                                  colour=discord.Colour.from_rgb(255, 255, 0))
                embed_msg.timestamp = datetime.utcnow()
                embed_msg.set_footer(text="RaDkon")
                await ctx.channel.purge(limit=2)
                await ctx.channel.send(embed=embed_msg)
                logging.info(f"\n\nUstawiono status bota na: Prace techniczne.\n\n")
            if param == "przerwa":
                activity = discord.Game(name="Mała przerwa..")
                status_bot = discord.Status.do_not_disturb
                await self.change_presence(status=status_bot, activity=activity)
                embed_msg = embed(title="Status bota:",
                                  description="*Przerwa*: :no_entry:",
                                  colour=discord.Colour.from_rgb(255, 0, 0))
                embed_msg.timestamp = datetime.utcnow()
                embed_msg.set_footer(text="RaDkon")
                await ctx.channel.purge(limit=2)
                await ctx.channel.send(embed=embed_msg)
                logging.info(f"\n\nUstawiono status bota na: Przerwa.\n\n")

    def reaction_role_chanel(self):
        @self.command(name="plec")
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

        @self.command(name="wiek")
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

        @self.command(name="gry")
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

        @self.event
        async def on_raw_reaction_add(payload):
            message_regulamin = 999688170927042643
            message_plec = 996145295014502410
            message_wiek = 996147074322153513
            message_gry = 996149490119618580
            message_przeczytaj_to = 996854970764754954
            guild = self.get_guild(payload.guild_id)
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

        @self.event
        async def on_raw_reaction_remove(payload):
            message_regulamin = 999688170927042643
            message_plec = 996145295014502410
            message_wiek = 996147074322153513
            message_gry = 996149490119618580
            message_przeczytaj_to = 996854970764754954
            guild = self.get_guild(payload.guild_id)
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

    def moderate(self):
        @self.command(name="kick")
        @has_permissions(kick_members=True)
        async def kick(ctx, username: member, *, reason="brak powodu"):
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
                text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!kick <Użytkownik> <powód>.`'
                await ctx.channel.send(text)
                logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !kick ({msg_user}).\n")
            if isinstance(error, MissingPermissions):
                text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
                await ctx.channel.send(text)
                logging.error(
                    f"\n\nUżytkownik {user_error} próbwował kogoś wyrzuć za pomocą komendy !kick ({msg_user}).\n")

        @self.command(name="ban")
        @has_permissions(ban_members=True)
        async def ban(ctx, username: member, *, reason="brak powodu", delete_message_days=7):
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
                text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!ban <Użytkownik> <powód>.'
                await ctx.channel.send(text)
                logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !ban ({msg_user}).\n")
            if isinstance(error, MissingPermissions):
                text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
                await ctx.channel.send(text)
                logging.error(
                    f"\n\nUżytkownik {user_error} próbwował kogoś zbanować za pomocą komendy !ban ({msg_user}).\n")

        @self.command(name="unban")
        @has_permissions(ban_members=True)
        async def unban(ctx, username: discord.User, *, reason="brak powodu"):
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
                text = f'<@{user_error.id}>, źle użyłeś komendy, spóbuj `!unban <Użytkownik> <powód>.`'
                await ctx.channel.send(text)
                logging.error(f"\n\nUżytkownik {user_error} źle użył komendy !unban ({msg_user}).\n")
            if isinstance(error, MissingPermissions):
                text = f"<@{user_error.id}>, niestety nie masz uprawnień do tego!"
                await ctx.channel.send(text)
                logging.error(
                    f"\n\nUżytkownik {user_error} próbwował kogoś odbanować za pomocą komendy !unban ({msg_user}).\n")

# file.close()
