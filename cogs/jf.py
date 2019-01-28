import asyncio
import logging
import traceback

from discord.ext import commands
from discord.colour import Color
from discord.embeds import Embed

import re

log = logging.getLogger(__name__)

class JF:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def jf(self, ctx, dest, volume):
        """
        Calculates the cost by m3 for GreenSwarm Express contracts. Valid destinations at this point are: d-o, do, home, d-ojez, and jita
        """
        priceIn = 800
        priceOut = 500
        minimumValue = 5000000

        allowedIn = ['d-o', 'home', 'do', 'd-ojez']
        allowedOut = ['jita']

        if dest in allowedIn:
            costs = int(priceIn) * int(volume)
        elif dest in allowedOut:
            costs = int(priceOut) * int(volume)
        else:
            return await ctx.send('Please select a valid destination. For now, the only valid destnations are \'d-o\', \'home\', \'do\', \'d-ojez\', \'jita\'')
        if int(costs) < int(minimumValue):
            costs = 5000000
        embed = Embed(title='Cost to transport {} m3 to {}: {:,} isk'.format(volume, dest, costs))
        embed.color = Color.green()

        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(JF(bot))
