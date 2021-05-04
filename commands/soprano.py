import discord
import random
import logging
from discord.ext import commands

import commands.ext.games as games

logger = logging.getLogger(__name__)


class SopranoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = games.GameManager(states=['ignore', 'shot'])

    @commands.command(name="сопрано", help="русская рулетка")
    async def execute(self, ctx):
        embed = discord.Embed(
            title="Русская рулетка", description="🎲 Испытай свою удачу!", colour=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await message.add_reaction('🔫')
        self.manager.add_session(games.GameSession(self.manager, message, 1, 99, 1))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user or reaction.emoji != '🔫':
            return
        message = reaction.message
        session = self.manager.get_session(message.id)
        # Сообщение - не игровая сессия
        if not session:
            return
        state = await self.process_game(session=session, user=user)
        if state == 'ignore':
            return

        embed = discord.Embed(
            title="Русская рулетка", description="🎲 Испытай свою удачу!", colour=discord.Color.green())

        for player in session.players:
            if not player.dead:
                embed.add_field(name=player.name,
                                value="🎉 Выжил", inline=False)
            else:
                embed.add_field(name=player.name,
                                value="☠️ Застрелился", inline=False)
                embed.colour = discord.Color.red()
                await message.clear_reactions()
        await message.edit(embed=embed)

    @games.handler
    async def process_game(self, **kwargs):
        user = kwargs.get('user')
        session = kwargs.get('session')
        if user in session.players:
            return 'ignore'
        session.players.append(games.GamePlayer(user, dead=self.possibly()))
        if session.players.current.dead:
                self.manager.remove_session(session.message.id)
        return 'shot'

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.manager.remove_session(message.id)

    async def cog_command_error(self, ctx, error):
        logger.exception(error)

    def possibly(self):
        return random.randint(0, 100) <= 17


def setup(bot):
    bot.add_cog(SopranoCommand(bot))
