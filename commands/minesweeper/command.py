import discord
import logging
import utils.helper as helper
import commands.ext.games as games
from discord.ext import commands
from .grid import GameGrid

logger = logging.getLogger(__name__)


class MinesweeperCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = bot.get_cog('GameManager')

    @commands.check_any(commands.guild_only())
    @commands.command(name="сапер", help="игра")
    async def execute(self, ctx, size: int = 6):
        grid = GameGrid(size)

        embed = discord.Embed(title="Сапер", description=str(
            grid), colour=discord.Color.blue())
        embed.add_field(
            name="Помощь", value="Чтобы походить, отправь мне код клетки (например, c4)\nЧтобы пометить клетку флагом, добавь в конце f (например, c4f)", inline=False)

        message = await ctx.send(embed=embed)
        session = games.GameSession(self.manager, message, 1, 4, grid=grid)
        session.add_handler('on_message', self.on_message)
        session.launch()
        self.manager.add_session(session)

    async def on_message(self, session, message, user):
        grid = session.grid
        if not grid.move(message.content):
            return

        await message.delete()

        embed = discord.Embed(title="Сапер", description=str(
            grid), colour=discord.Color.blue())

        if not grid.completed:
            embed.add_field(
                name="Последний ход", value=f"{user.display_name} делает ход {message.content.upper()}")
        else:
            session.close()
            if grid.lost:
                embed.add_field(name="Игра завершена", value="Вы проиграли!")
                embed.colour = discord.Color.red()
            else:
                embed.add_field(name="Игра завершена", value="Вы выиграли!")
                embed.colour = discord.Color.green()
        await session.message.edit(embed=embed)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=helper.get_error_embed(desc="Команда доступна только на серверах"))
        logger.exception(error)


def setup(bot):
    bot.add_cog(MinesweeperCommand(bot))
