from random import randint
import discord
import asyncio
import logging
from discord.ext import commands
import re

import config
from discord import embeds, Color

log = logging.getLogger(__name__)


class Roll:
    def __init__(self, bot):
        self.bot = bot

# @commands.group(pass_context=True)
# @commands.guild_only()
# async def roll(self, ctx, *, roll)
#  if ctx.invoked_subcommand is None:
#   await ctx.invoke(self.raw, roll=ctx.message.content[7:]

    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx, *, roll):
        match = re.match('^[1-9]\d{0,3}d[1-9]\d{0,3}\+[0-9]\d{0,3}$', roll)

        if match:
            nDice, nSides, modifier = re.split('d|\+', roll)
            nDice = int(nDice)
            nSides = int(nSides)
            modifier = int(modifier)

            rTotal = 0
            for side in range(nSides):
                r = randint(1, nSides)
                results = rTotal + r

            nResult = results + modifier
            print(nResult)

        else:
            return await ctx.message.add_reaction(chr(0x274c))

# @roll.command()
# @commands.guild_only()
# async def hit(self, ctx, *, roll)


def setup(bot):
    bot.add_cog(Roll(bot))
