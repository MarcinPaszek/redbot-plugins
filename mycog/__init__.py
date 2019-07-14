from .mycog import Mycog
from .weather import Weather

def setup(bot):
    bot.add_cog(Mycog())
    bot.add_cog(Weather())