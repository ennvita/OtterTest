import asyncio
import logging
import traceback

import re
import pendulum
from tinydb import TinyDB, Query

from discord.ext import commands
from discord.colour import Color
from discord.embeds import Embed
from discord.utils import get

log = logging.getLogger(__name__)

class Remind:
    def __init__(self, bot):
        self.bot = bot
        self.format_message = 'Accepted format: {time} - {message}. ex. o.remindme 2 hours - astra armor timer'


    @commands.command(pass_context=True, aliases=['remindme', 'reminder'])
    async def remind(self, ctx, *, rem):
        if ctx.invoked_subcommand is None:
            try:
                time, message = rem.split(' - ')
                if not time or not message:
                    raise commands.MissingArgument(self.format_message)
            except ValueError:
                raise commands.BadArgument(self.format_message)
        if len(message) > 500:
            raise commands.BadArgument('Message is too long.')

        remind_time = pendulum.parse(time, strict=False)
        now = pendulum.now()
        if remind_time <= now:
            future = now - remind_time
            remind_time = remind_time + future + future
        print(remind_time, now)


def setup(bot):
    bot.add_cog(Remind(bot))
