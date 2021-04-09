import discord

colors = { 'info':discord.Color.blue(), 'success':discord.Color.green(), 'warning':discord.Color.gold(), 'error':discord.Color.red() }

def get_discord_color(type = 'info'):
    return colors.get(type, 'info')

def get_error_embed(desc):
    return discord.Embed(description = "🤷 {}".format(desc), colour = get_discord_color('error'))
