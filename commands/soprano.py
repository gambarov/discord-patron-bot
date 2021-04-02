import discord, random, logging
from discord.ext import commands
from utils.helper import get_discord_color

logger = logging.getLogger('discord')

class SopranoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}

    @commands.command(name = "сопрано", help = "русская рулетка")
    async def execute(self, ctx):
        embed = discord.Embed(title = "Русская рулетка", description = "Испытай свою удачу!", colour = get_discord_color('info'))
        message = await ctx.send(embed = embed)
        await message.add_reaction('🔫')
        self.sessions[message.id] = { 'id':message.id, 'users':[] }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        if reaction.emoji != '🔫':
            return

        message = reaction.message
        session = self.sessions.get(message.id, None)
        # Сообщение - не игровая сессия
        if not session:
            return
        # Пользователь уже поучаствовал
        if user in session['users']:
            return
        session['users'].append(user)

        embed = discord.Embed(title = "Русская рулетка", description = "Испытай свою удачу!", colour = get_discord_color('success'))
        # Добавляем сообщения о других участниках
        for field in message.embeds[0].fields:
            embed.add_field(name = field.name, value = field.value, inline = False)

        name = "{}#{}".format(user.name, user.discriminator)
        
        if (self.possibly()):
            embed.add_field(name = name, value = "❌ Застрелился", inline = False)
            embed.colour = get_discord_color('error')
            embed.set_footer(text = "Игра завершена")
            del self.sessions[message.id]
            await message.clear_reactions()
        else:
            embed.add_field(name = name, value = "🎉 Выжил", inline = False)
        await message.edit(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        session = self.sessions.get(message.id, None)
        if session:
           del self.sessions[message.id]

    async def cog_command_error(self, ctx, error):
        logger.exception(error)
        await ctx.send(embed = discord.Embed(description = "Неизвестная ошибка!", colour = get_discord_color('error')))

    def possibly(self):
        return random.randrange(1, 100) <= 17

def setup(bot):
    bot.add_cog(SopranoCommand(bot))