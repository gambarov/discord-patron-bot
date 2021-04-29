import discord

PRIVATE = False

intents = discord.Intents().all()

def options():
    if PRIVATE:
        return { 'command_prefix':'_', 'intents':intents }
    return { 'command_prefix':('!'), 'intents':intents, 'help_command':None }