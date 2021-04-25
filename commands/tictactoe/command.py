from discord.ext import commands
import discord
import logging
import utils.helper as helper

from commands.tictactoe.manager import GameManager
from commands.tictactoe.grid import GameGrid

logger = logging.getLogger(__name__)

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = GameManager()

    @commands.command(name="тик", help="крестики-нолики!")
    @commands.check_any(commands.guild_only())
    async def execute(self, ctx):
        grid = GameGrid()

        embed = discord.Embed(
            title="Крестики-нолики", description=str(grid), colour=helper.get_discord_color('info'))
        embed.set_footer(text="⚙️ Подготовка сессии, подождите...")

        message = await ctx.send(embed=embed)

        for i in range(len(grid.matrix)):
            for j in range(len(grid.matrix[i])):
                emoji = grid.matrix[i][j]['emoji']
                await message.add_reaction(emoji)

        embed.set_footer(text="👀 Ожидание игроков...")
        await message.edit(embed=embed)
        self.manager.add_session(message_id=message.id, grid=grid)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Игнорируем себя (бота)
        if user == self.bot.user:
            return
        message = reaction.message
        session = self.manager.sessions.get(message.id, None)
        # Если сообщение - не сессия игры
        if not session:
            return
        grid = session.grid
        # В клетку уже походили
        if not grid.has(reaction.emoji):
            return
        # Получаем текущего игрока
        player = session.move_next(user)
        # Текущий юзер - не (текущий) игрок
        if not player:
            return
        # Убираем кнопку с ячейкой
        await message.clear_reaction(reaction.emoji)
        # Помечаем на поле
        grid.replace(reaction.emoji, player.emoji)

        embed = discord.Embed(
            title="Крестики-нолики", description=str(grid), colour=helper.get_discord_color('info'))

        embed.add_field(name="Игрок №1",
                        value="<@!{}>".format(session.first.user.id))
        embed.add_field(name="Игрок №2", value="Ожидается" if not session.ready(
        ) else "<@!{}>".format(session.second.user.id))

        winner = self.manager.check_for_winner(session)
        if winner:
            embed.add_field(name="🏆 Победитель:",
                            value="<@!{}>".format(winner.user.id), inline=False)
            embed.colour = helper.get_discord_color('success')
            self.manager.delete_session(message.id)
        elif self.manager.check_for_draw(session):
            embed.add_field(name="Игра завершена",
                            value="🍻 Ничья!", inline=False)
            embed.colour = helper.get_discord_color('warning')
            self.manager.delete_session(message.id)
        else:
            # Получаем инфу о след игроке
            pnext = session.first if session.previous == session.second else session.second
            if pnext:
                embed.add_field(name="Текущий ход", value="{} ({})".format(
                    "<@!{}>".format(pnext.user.id), pnext.emoji), inline=False)
        await message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        session = self.manager.sessions.get(message.id, None)
        if session:
            self.manager.delete_session(message.id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed=helper.get_error_embed(desc="Размер поля должен быть целым числом"))
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=helper.get_error_embed(desc="Команда доступна только на серверах"))
        logger.exception(error)


def setup(bot):
    bot.add_cog(TicTacToe(bot))
