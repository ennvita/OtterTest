import pendulum
import re
from tinydb import TinyDB, Query

from discord.ext import commands
from discord.colour import Color
from discord.embeds import Embed

import logging
import traceback
import asyncio

log = logging.getLogger(__name__)
db = TinyDB('db.json')


class Who:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def who(self, ctx, *, character):


def setup(bot):
    bot.add_cog(Who(bot))
