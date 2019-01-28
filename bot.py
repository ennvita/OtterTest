import logging
import sys
import traceback

import aiohttp
import aioredis
import pendulum
from discord.ext import commands
import discord

from cogs.utils import context
from cogs.utils.esi import ESI

try:
    import config
except ImportError:
    print("Config not found")
    sys.exit(1)

description = """ Ottersquad #1 """

log = logging.getLogger(__name__)

initial_cogs = (
    'cogs.joinrole',
    'cogs.roll',
    'cogs.addrole',
    'cogs.weather',
    'cogs.time',
#    'cogs.who',
    'cogs.order',
    'cogs.someone',
    'cogs.mumble',
    'cogs.jf',
    'cogs.remind',
    'cogs.jump',

)


class OtterBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            description=description,
            pm_help=False,
            help_attrs=dict(hidden=True))

        self.client_id = config.client_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.esi = ESI()

        self.add_command(self.uptime)
#  self.add_command(self.invite)
        self.add_command(self._reload)
        self.add_command(self.load)
        self.add_command(self.unload)

        for cog in initial_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Failed to load cog {cog}', file=sys.stderr)
                traceback.print_exc()

    async def start_redis(self):
        self.redis = await aioredis.create_pool(
            ('localhost', 6379), minsize=5, maxsize=10, loop=self.loop)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in PMs')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('This command has been disabled')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)

    async def on_ready(self):
        if not hasattr(self, 'currentuptime'):
            await self.start_redis()
            self.currentuptime = pendulum.now(tz='UTC')
            print('Ready')

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:
            return
        await self.invoke(ctx)

    async def on_message(self, message):
        message.content = message.content.lower()
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_resumed(self):
        print('Otter Bot is back in action.')

    def run(self):
        super().run(config.token, reconnect=True)

    @property
    def config(self):
        return __import__('config')

    @commands.command(pass_context=True, hidden=True)
    async def uptime(self, ctx):
        """ Returns OtterBot's uptime. """
        await ctx.send(pendulum.now(tz='UTC').diff_for_humans(self.currentuptime, absolute=True))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog):
        """Reloads a cog"""
        try:
            self.unload_extension(cog)
            self.load_extension(cog)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """Loads a cog"""
        try:
            self.load_extension(cog)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """Unloads a cog"""
        try:
            self.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def invite(self, ctx):
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.manage_roles = True
        perms.manage_channels = True
        perms.ban_members = False
        perms.kick_members = False
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.add_reactions = True
        await ctx.send(f'<{discord.utils.oauth_url(self.client_id, perms)}>')
