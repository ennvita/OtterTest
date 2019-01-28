import logging
import traceback

from opencage.geocoder import OpenCageGeocode
from darksky import forecast
from discord.ext import commands
from discord import embeds, Color
import config

log = logging.getLogger(__name__)
deg = u'\u00b0'


class Weather:
    def __init__(self, bot):
        self.bot = bot
        self.geocoder = OpenCageGeocode(key=config.opencage_key)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def weather(self, ctx, *, city):
        # """
        # Gives the current weather of the specified location
        # """
        if not city:
            raise commands.MissingRequiredArgument("Add a city, nincompoop.")

        g = self.geocoder.geocode(city)
        print(g)
        if not g:
            raise commands.BadArgument("City not found")
        lat = g[0]['geometry']['lat']
        lng = g[0]['geometry']['lng']

        with forecast(config.weather_api, lat, lng) as myforecast:
            embed = embeds.Embed(
                title=g[0]['formatted'], url=f'https://darksky.net/forecast/{lat}/{lng}', description=myforecast.daily.summary)
            embed.set_footer(text='https://darksky.net/poweredby/')
            embed.add_field(name='Current Temperature:', value='{}\n{}F ({:.1f}C)'.format(
                myforecast.currently.summary, myforecast.currently.temperature, (myforecast.currently.temperature - 32) * (5 / 9)))
            embed.add_field(name='Feels like:', value='{}F ({:.1f}C)'.format(
                myforecast.currently.apparentTemperature, (myforecast.currently.apparentTemperature - 32) * (5 / 9)))
            embed.add_field(name='Alerts:', value=myforecast.alerts[0].title)
            embed.add_field(name='Precipitation Type:', value=myforecast.currently.precipType)

        return await ctx.send(embed=embed)

    async def __error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        else:
            traceback.print_tb(error.original.__traceback__)
            print(error)


def setup(bot):
    bot.add_cog(Weather(bot))
