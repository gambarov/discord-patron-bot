from discord.ext import commands

def is_cartel():
    def predicate(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.id == 629271591762657346
    return commands.check(predicate)
