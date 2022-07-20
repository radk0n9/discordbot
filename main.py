
# TODO 3 Message when someone boost the server

import discord
import sys
import datetime as dt
from my_client import MyClient
from event import SendMessage, OnMember, OnMemberUpdate
from role_dict import ROLE_DICT_PLEC, ROLE_DICT_WIEK, ROLE_DICT_GRY
from discord.ext.commands import has_permissions, MissingPermissions

file = open("log.txt", "a")
sys.stdout = file
now = dt.datetime.now()
date_time = now.strftime("%d-%m-%Y, %H:%M:%S")

intents = discord.Intents.all()
client = MyClient(command_prefix="!", intents=intents, self_bot=False)


embed = discord.Embed
user = discord.User
message = discord.Message

client.clearing()
client.list_users()
client.report_a_problem()


@client.event
async def on_message(msg):
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
        print(f"Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await payload.member.add_roles(role)
        print(f"Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await payload.member.add_roles(role)
                print(f"Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await payload.member.add_roles(role)
                print(f"Dodano role {role} - {payload.member.name}")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await payload.member.add_roles(role)
                print(f"Dodano role {role} - {payload.member.name}")


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
        print(f"Usunieto role {role} - {member.name}")

    if payload.message_id == message_przeczytaj_to:
        role = discord.utils.get(guild.roles, name="Beta-Tester")
        await member.remove_roles(role)
        print(f"Usunieto role {role} - {member.name}")

    if payload.message_id == message_plec:
        for rola in ROLE_DICT_PLEC:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_PLEC[rola])
                await member.remove_roles(role)
                print(f"Usunieto role {role} - {member.name}")

    if payload.message_id == message_wiek:
        for rola in ROLE_DICT_WIEK:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_WIEK[rola])
                await member.remove_roles(role)
                print(f"Usunieto role {role} - {member.name}")

    if payload.message_id == message_gry:
        for rola in ROLE_DICT_GRY:
            if payload.emoji.name == rola:
                role = discord.utils.get(guild.roles, name=ROLE_DICT_GRY[rola])
                await member.remove_roles(role)
                print(f"Usunieto role {role} - {member.name}")

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
file.close()
