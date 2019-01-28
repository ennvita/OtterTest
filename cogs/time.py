import asyncio
import logging

import dateparser
import pendulum
import traceback
from discord.ext import commands

from discord import embeds

log = logging.getLogger(__name__)


class Time:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def time(self, ctx):
        """ Current Eve Time """

        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                await asyncio.sleep(.5)
                return await ctx.send(embed=embeds.Embed(title='Current EVE Time:', description=pendulum.now(tz='UTC').to_datetime_string()))

    # @time.command()
    # async def local(self, ctx, *, time):
    # async with ctx.typing():
    #  await asyncio.sleep(.5)
    #  return await ctx.send(embed.embeds.Embed(title='Returns User\'s Local time', description=pendulum.now(

# @time.command()
# async def until(self, ctx, *, time):

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        else:
            traceback.print_tb(error.original.__traceback__)
            print(error)


def setup(bot):
    bot.add_cog(Time(bot))
