import asyncio
import logging
#import requests
import traceback

from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get

log = logging.getLogger(__name__)


class AddRole:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_role(name='madmin')
    async def addrole(self, ctx, *, role):
        with open('cogs/utils/roles.txt', 'a', encoding='utf8') as rolef:
            rolef.write(f'{role}\n')

#   defaultPerms = ctx.message.author.Permissions(read_messages=True, send_messages=True, embed_links=True, add_reactions=True, attach_files=True, external_emojis=True)
            category = discord.utils.get(
                ctx.message.guild.categories, id=410169384623931392)
            await ctx.message.guild.create_text_channel(f'{role}', category=category)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.has_role(name='madmin')
    async def removerole(self, ctx, *, role):
        with open('cogs/utils/roles.txt', 'r+', encoding='utf8') as rolef:
            rolesList = rolef.read().splitlines()

            rolesList.remove(f'{role}')

            rolef.seek(0)
            rolef.truncate()

            for roles in rolesList:
                rolef.write(roles + '\n')


def setup(bot):
    bot.add_cog(AddRole(bot))
