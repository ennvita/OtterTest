import asyncio
import traceback
import logging

import discord
from discord.ext import commands
from discord.colour import Color
from discord.embeds import Embed

import socket
from datetime import datetime
from struct import *

class Mumble:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def mumble(self, ctx, *, server_name):
        if not server_name:
            raise commands.MissingRequiredArgument()
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.settimeout(1)
        buf = pack(">iQ", 0, datetime.now().microsecond)
        try:
            new_socket.sendto(buf, (server_name, 64738))
            data, addr = new_socket.recvfrom(1024)
        except:
            return await ctx.message.add_reaction(self.bot.no_emoji)
        r = unpack(">bbbbQiii", data)
        return await ctx.send(f"Users: **{r[5]}/{r[6]}**")
def setup(bot):
    bot.add_cog(Mumble(bot))
