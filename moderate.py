# import discord
# import logging
# from my_client import MyClient
# from discord.ext.commands import has_permissions, MissingPermissions, MemberNotFound, MissingRequiredArgument, cooldown,\
#     BucketType, CommandOnCooldown
#
# intents = discord.Intents.all()
# intents.members = True
# client = MyClient(command_prefix="!", intents=intents, self_bot=False)
#
# embed = discord.Embed
# user = discord.User
# message = discord.Message
# member = discord.Member
#
#
# class Kick:
#     def kick_user():
#         @client.command(name="kick")
#         @has_permissions(kick_members=True)
#         async def kick(self, username: member, *, reason):
#             logging.warning(f"\n\n{self.message.author.name} wyrzucił {username.display_name} za: {reason}.\n")
#             await self.channel.purge(limit=1)
#             await username.kick(reason=reason)
#             await self.channel.send(f"<@{self.message.author.id}> wyrzucił {username.display_name} za: **{reason}**.")
#
#
#



