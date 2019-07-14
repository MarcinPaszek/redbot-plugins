from .mycog import Mycog
from .weather import Weather

def setup(bot):
    n=Mycog(bot)
    bot.add_cog(n)
    m=Weather(bot)
    bot.add_cog(m)