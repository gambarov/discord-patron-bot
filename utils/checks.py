import discord
from discord.ext import commands

class PremiumRequired(commands.CheckFailure):
    pass

def is_cartel(ctx):
    if not isinstance(ctx.channel, discord.TextChannel):
        return False
    if not ctx.channel.category:
        return False
    return ctx.channel.category.id == 816337597113958411

def is_test_channel(channel):
    return channel.id == 823542321328947232

# TODO:
def is_vip_user():
    async def predicate(ctx):
        if not is_cartel(ctx) or not ctx.author.id == 627833817708625931:
            raise PremiumRequired
        return True
    return commands.check(predicate)