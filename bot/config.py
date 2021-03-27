import discord

intents = discord.Intents().default()
intents.members = True

options = { 'command_prefix':'!', 'intents':intents }