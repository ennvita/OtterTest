import asyncio
import logging
import traceback

import discord
from discord.ext import commands

import random

log = logging.getLogger(__name__)

class Someone:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def someone(self, ctx):
        memList = []
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name == 'Autismo Crew':
                    memList.append(member)
        rUser = random.choice(memList)
        forms = ['{}, I choose you!', '{} has been chosen!']
        cForm = random.choice(forms)
        return await ctx.send(cForm.format(rUser.mention))

def setup(bot):
    bot.add_cog(Someone(bot))
