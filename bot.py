import os

import discord
import random

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith('!кто'):
        member = random.choice(message.channel.members)
        content = message.content.split(' ', 1)[1]
        await message.channel.send("Бля буду, " + member.name + " " + content)


client.run(TOKEN)