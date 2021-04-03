import discord

_discord_colors = { 'info':0x4299F5, 'success':0x42F56C, 'warning':0xF59E42, 'error':0xE02B2B }

def get_discord_color(type = 'info'):
    return _discord_colors.get(type, 'info')

def get_error_embed(desc):
    return discord.Embed(description = "🤷 {}".format(desc), colour = get_discord_color('error'))
