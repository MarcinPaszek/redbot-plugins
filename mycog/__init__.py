from .mycog import Mycog

def setup(bot):
    bot.add_cog(Mycog())
    bot.add_cog(Weather())
