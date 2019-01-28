import asyncio
import json
import logging
import re
import traceback
import urllib.request
import hashlib

import gspread
import pendulum
import requests
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from gspread import models
from oauth2client.service_account import ServiceAccountCredentials

log = logging.getLogger(__name__)

class Order:
    def __init__(self, bot):
        self.bot = bot

    def check_guild(ctx):
        allowed_guilds = [369733205194178562, 345270396058075137, 430145179215724545, 317746493060808704]
        return ctx.author.guild.id in allowed_guilds

    def is_jf(ctx):
        allowed_pilots = [362630071200120834, 106290263441342464]
        return ctx.author.id in allowed_pilots

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.check(check_guild)
    async def order(self, ctx, order, *, comment):
        """
        Places an order with the GreenSwarm jf service. Format: o.order <evepraisal link> your comments go here.
        """
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets',
                                     'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                                    '/home/zoro/OtterBot/google_secret.json', scope)
            gc = gspread.authorize(creds)
        except APIError as response:
            print(response)

        try:
          shop = gc.open_by_key('16dYWGvfwNOkx3Pf27rrp7yJyX6D3zOtkmm2uOj3Nnis').sheet1
        except APIError as response:
            print(response)
    
        def next_available_row(shop):
            row_filter = list(filter(None, shop.col_values(1)))
            row_num = len(row_filter) + 1
            return row_num

        if re.match('^.*evepraisal.com\/a\/.*$', order):
            jOrder = order + '.json'
            with urllib.request.urlopen(f'{jOrder}') as url:
                orderData = json.loads(url.read().decode())
                itemData = orderData['items']
                purchaserID = ctx.message.author.display_name
                item_cell = []
                row_num = next_available_row(shop)
                for item in itemData:
                    item_cell.append(gspread.Cell(row_num, 1, item['name']))
                    item_cell.append(gspread.Cell(row_num, 2, item['quantity']))
                    item_cell.append(gspread.Cell(row_num, 3, item['prices']['all']['avg']))
                    item_cell.append(gspread.Cell(row_num, 4, purchaserID))
                    item_cell.append(gspread.Cell(row_num, 5, f'{comment}'))
                    row_num += 1
                try:
                    shop.update_cells(item_cell)
                    order_gap = []
                    order_gap.append(gspread.Cell(next_available_row(shop), 1, '-'))
                    shop.update_cells(order_gap)
                except Exception as err:
                    print(err)
            return await ctx.message.add_reaction(chr(0x1f44d))
        elif re.match('^.*zkillboard.com\/kill\/.*$', order):
            match = re.findall('\d\d\d\d\d\d\d\d', order)
            zkillID = match[0]
            jkOrder = f'https://zkillboard.com/api/killID/{zkillID}/'
            with urllib.request.urlopen(f'{jkOrder}') as url:
                orderData = json.loads(url.read().decode())
                ekillID = orderData[0]['killmail_id']
                ekillHash = orderData[0]['zkb']['hash']
                
                try:
                    kill_op = self.bot.esi.esi.get_operation('get_killmails_killmail_id_killmail_hash')
                    killsheet = kill_op.json(killmail_id=ekillID, killmail_hash=ekillHash)
                except Exception as e:
                    print(e)
                kill_items = killsheet['victim']['items']
                ship = killsheet['victim']['ship_type_id']
                item_cell = []
                row_num = next_available_row(shop)
                for item_type_id in kill_items:
                    print(item_type_id)

            return await ctx.message.add_reaction(chr(0x1f44d))
        else: 
            return await ctx.send('Order must be an Evepraisal or Zkill link.')

    @commands.command(pass_context=True, hidden=True)
    @commands.guild_only()
    @commands.check(is_jf)
    async def clearlist(self, ctx):
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets',                                                                                        'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                    '/home/zoro/OtterBot/google_secret.json', scope)
            gc = gspread.authorize(creds)
        except Exception as e:
            print(e)
        try:
            shop = gc.open_by_key('16dYWGvfwNOkx3Pf27rrp7yJyX6D3zOtkmm2uOj3Nnis').sheet1
        except Exception as e:
            print(e)
        shop.resize(rows=1)
        shop.resize(rows=1000)
        return await ctx.message.add_reaction(chr(0x1f44d))


def setup(bot):
    bot.add_cog(Order(bot))
