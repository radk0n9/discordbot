import discord
import logging
from datetime import datetime
from discord.ext import commands
from role_dict import ROLE_DICT_PLEC, ROLE_DICT_WIEK, ROLE_DICT_GRY

embed = discord.Embed
guild = discord.Guild
user = discord.User
message = discord.Message
member = discord.Member


class ReactionRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_regulamin = 999688170927042643
        message_plec = 996145295014502410
        message_wiek = 996147074322153513
        message_gry = 996149490119618580
        message_przeczytaj_to = 996854970764754954
        guild = self.client.get_guild(payload.guild_id)
        # member = guild.get_member(payload.user_id)

        if payload.message_id == message_regulamin:
            role = discord.utils.get(guild.roles, name="☑️")
            await payload.member.add_roles(role)
            logging.info(f"Dodano role {role} - {payload.member.name}.")

        if payload.message_id == message_przeczytaj_to:
            role = discord.utils.get(guild.roles, name="Beta-Tester")
            await payload.member.add_roles(role)
            logging.info(f"Dodano role {role} - {payload.member.name}.")

        if payload.message_id == message_plec:
            for rola in ROLE_DICT_PLEC:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                    await payload.member.add_roles(role)
                    logging.info(f"Dodano role {role} - {payload.member.name}.")

        if payload.message_id == message_wiek:
            for rola in ROLE_DICT_WIEK:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                    await payload.member.add_roles(role)
                    logging.info(f"Dodano role {role} - {payload.member.name}.")

        if payload.message_id == message_gry:
            for rola in ROLE_DICT_GRY:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                    await payload.member.add_roles(role)
                    logging.info(f"Dodano role {role} - {payload.member.name}.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_regulamin = 999688170927042643
        message_plec = 996145295014502410
        message_wiek = 996147074322153513
        message_gry = 996149490119618580
        message_przeczytaj_to = 996854970764754954
        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.message_id == message_regulamin:
            role = discord.utils.get(guild.roles, name="☑️")
            await member.remove_roles(role)
            logging.info(f"Usunieto role {role} - {member.name}.")

        if payload.message_id == message_przeczytaj_to:
            role = discord.utils.get(guild.roles, name="Beta-Tester")
            await member.remove_roles(role)
            logging.info(f"Usunieto role {role} - {member.name}.")

        if payload.message_id == message_plec:
            for rola in ROLE_DICT_PLEC:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                    await member.remove_roles(role)
                    logging.info(f"Usunieto role {role} - {member.name}.")

        if payload.message_id == message_wiek:
            for rola in ROLE_DICT_WIEK:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                    await member.remove_roles(role)
                    logging.info(f"Usunieto role {role} - {member.name}.")

        if payload.message_id == message_gry:
            for rola in ROLE_DICT_GRY:
                if payload.emoji.name == rola:
                    role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                    await member.remove_roles(role)
                    logging.info(f"Usunieto role {role} - {member.name}.")

    @commands.command(name="plec")
    @commands.has_permissions(administrator=True)
    async def plec(self, ctx, amount=1):
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

    @commands.command(name="wiek")
    @commands.has_permissions(administrator=True)
    async def wiek(self, ctx, amount=1):
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

    @commands.command(name="gry")
    @commands.has_permissions(administrator=True)
    async def gry(self, ctx, amount=1):
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


def setup(client):
    client.add_cog(ReactionRole(client))
