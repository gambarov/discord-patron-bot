import discord

PRIVATE = False

intents = discord.Intents().all()
options = { 'command_prefix':('!' if not PRIVATE else '$'), 'intents':intents, 'help_command':None }