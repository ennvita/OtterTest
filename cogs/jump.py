import asyncio
import logging
import traceback

import re

from discord.ext import commands
from discord.colour import Color
from discord.embeds import Embed

log = logging.getLogger(__name__)

class Jump:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def jump(self, ctx, origin, dest, ship):
        if not origin:
            raise commands.BadArgument('Missing required argument: \'origin\'.')
        if not dest:
            raise commands.BadArgument('Missing required argument: \'destination\'.')
        if not ship:
            raise commands.BadArgument('Missing required argument: \'ship\'')
        origin = origin.capitalize()
        dest = dest.capitalize()
        ship = ship.capitalize()

        await ctx.trigger_typing()
        try:
            try:
                origin_lookup = self.bot.esi.search('solar_system', origin)
                origin_id = origin_lookup['solar_system'][0]
            except KeyError:
                embed = Embed(
                        title='Origin not found')
                embed.color = Color.red()
                return await ctx.send(embed=embed)
            try:
                dest_lookup = self.bot.esi.search('solar_system', dest)
                dest_id = dest_lookup['solar_system'][0]
                
                dest_sheet_operation = self.bot.esi.esi.get_operation('get_universe_systems_system_id')
                dest_sheet = dest_sheet_operation.json(system_id=dest_id)
                
                dest_sec = round(float(dest_sheet['security_status']), 2)
                if dest_sec >= .50:
                    raise commands.BadArgument('You cannot jump to a high security system.')
            except KeyError:
                embed = Embed(
                        title='Destination not found')
                embed.color = Color.red()
                return await ctx.send(embed=embed)


            try:
                ship_lookup = self.bot.esi.search('inventory_type', ship)
                ship_id = ship_lookup['inventory_type'][0]

                ship_sheet_operation = self.bot.esi.esi.get_operation('get_universe_types_type_id')
                ship_sheet = ship_sheet_operation.json(type_id=ship_id)

                dogma_attr = ship_sheet['dogma_attributes']
                if len(list(filter(lambda x: x['attribute_id'] == 861, dogma_attr))) == 1:
                    pass
                else:
                    embed = Embed(
                            title=f'The **{ship}** is not a jump capable ship.')
                    embed.color = Color.red()
                    embed.set_thumbnail(url=f'https://image.eveonline.com/Type/{ship_id}_64.png')
                    return await ctx.send(embed=embed)
            except KeyError:
                embed = Embed(
                        title='Ship not found')
                embed.color = Color.red()
                return await ctx.send(embed=embed)

            route = origin + ':' + dest
            skills = 555
            url = f'https://evemaps.dotlan.net/jump/{ship},{skills}/{route}'
            embed = Embed(
                    title=f'Jump Route for {ship}',
                    url=url)
            embed.set_thumbnail(url=f'https://image.eveonline.com/Type/{ship_id}_64.png')
            embed.add_field(name='Origin System',
                    value=f'{origin}', inline=False)
            embed.add_field(name='Destination System',
                    value=f'{dest}', inline=False)
            embed.set_footer(text='Skills used: Jump Drive Callibration = 5, Jump Fuel Conservation = 5, Jump Freighter = 5')
            embed.color = Color.green()
        except Exception as err:
            return await ctx.send(f'```py\n{traceback.format_exc()}\n```')

        return await ctx.send(embed=embed)

    async def __error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        else:
            traceback.print_tb(error.original.__traceback__)
            print(error)

def setup(bot):
    bot.add_cog(Jump(bot))
