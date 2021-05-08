import discord
import random
import logging
from discord.ext import commands

import commands.ext.games as games

logger = logging.getLogger(__name__)


class SopranoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = bot.get_cog('GameManager')

    @commands.command(name="сопрано", help="русская рулетка")
    async def execute(self, ctx):
        embed = discord.Embed(
            title="Русская рулетка", description="🎲 Испытай свою удачу!", colour=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await message.add_reaction('🔫')
        session = games.GameSession(self.manager, message, 1, 99, 1)
        session.add_handler('on_reaction_add', self.on_reaction_add)
        self.manager.add_session(session)

    async def on_reaction_add(self, session, reaction, user):
        if user in session.players or reaction.emoji != '🔫':
            return
        session.players.append(games.GamePlayer(user, dead=self.possibly()))

        embed = discord.Embed(
            title="Русская рулетка", description="🎲 Испытай свою удачу!", colour=discord.Color.green())

        message = session.message
        for player in session.players:
            if not player.dead:
                embed.add_field(name=player.name,
                                value="✌️ Выжил", inline=False)
            else:
                session.close()
                embed.add_field(name=player.name,
                                value="☠️ Застрелился", inline=False)
                embed.colour = discord.Color.red()
                await message.clear_reactions()
        await message.edit(embed=embed)

    async def cog_command_error(self, ctx, error):
        logger.exception(error)

    def possibly(self):
        return random.randint(0, 100) <= 17


def setup(bot):
    bot.add_cog(SopranoCommand(bot))
