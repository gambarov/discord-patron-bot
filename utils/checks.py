import discord
from discord.ext import commands

def is_cartel(ctx):
    if not isinstance(ctx.channel, discord.TextChannel):
        return False
    if not ctx.channel.category:
        return False
    return ctx.channel.category.id == 816337597113958411

# TODO:
def is_vip_user():
    def predicate(ctx):
        return is_cartel(ctx)
    return commands.check(predicate)