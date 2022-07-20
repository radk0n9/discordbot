# import discord
# import os
# from my_client import MyClient
# from role_dict import ROLE_DICT_PLEC, ROLE_DICT_WIEK, ROLE_DICT_GRY
# from discord.ext import commands
# from discord.ext.commands import has_permissions, MissingPermissions
# from dotenv import load_dotenv
#
# load_dotenv()
# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# intents = discord.Intents.all()
# # client = commands.Bot(command_prefix="!", intents=intents)
# client = MyClient(command_prefix="!", intents=intents)
# # embed = bot.embed()
#
# class Role:
#
#
#     def plec(self):
#         @client.command(name="plec")
#         async def plec(ctx, amount=1):
#             await ctx.channel.purge(limit=amount)
#             embed_msg = embed(title="Wybierz swoją płeć:",
#                               description="\n"
#                                           ":man_gesturing_no: : Mężczyzna\n"
#                                           "\n"
#                                           ":person_gesturing_no: : Kobieta\n",
#                               colour=discord.Colour.dark_magenta(),
#                               )
#             msg = await ctx.channel.send(embed=embed_msg)
#             emojis = ROLE_DICT_PLEC
#             for emoji in emojis:
#                 await msg.add_reaction(emoji)