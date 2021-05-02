import discord
import logging

import utils.helper as helper

from commands.tictactoe.grid import GameGrid
import commands.ext.games as games

from discord.ext import commands

logger = logging.getLogger(__name__)

emojis = ['❌', '⭕']


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = games.GameManager(
            ['ignore', 'preparing', 'playing', 'draw', 'won'])

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
        session = self.manager.add_session(message, 2, 2, 1, grid=grid)
        # Сразу переводим флаг, т.е. готовность при полном кол-ве игроков
        session.launch()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        message = reaction.message
        session = self.manager.get_session(message.id)
        # Сообщение - не сессия игры
        if not session:
            return

        state = await self.process_game(session=session, user=user, emoji=reaction.emoji)
        if state == 'ignore':
            return

        grid = session.grid

        embed = discord.Embed(
            title="Крестики-нолики", description=str(grid), colour=helper.get_discord_color('info'))

        def add_players_info(embed, session: games.GameSession, about_current: bool):
            players = session.players
            for index, player in enumerate(players):
                embed.add_field(name=f"Игрок #{index+1}", value=player.mention)
            if about_current and session.ready():
                # Получаем инфу о след игроке
                current = players.current
                if current:
                    embed.add_field(name="Текущий ход", value="{} ({})".format(
                        current.mention, current.emoji), inline=False)
            return embed

        players = session.players
        embed = add_players_info(
            embed, session, True if state == 'playing' else False)

        if state == 'preparing':
            embed.description = str(grid)
            embed.set_footer(text="👀 Ожидание игроков...")
        elif state == 'playing':
            pass
        else:
            # Партия закончена, можно очищать
            self.manager.remove_session(message.id)
            if state == 'won':
                winner = players.winners[0]
                embed.add_field(
                    name="🏆 Победитель:", value=winner.mention, inline=False)
                embed.colour = helper.get_discord_color('success')
            elif state == 'draw':
                embed.add_field(name="Игра завершена",
                                value="🍻 Ничья!", inline=False)
                embed.colour = helper.get_discord_color('warning')
        await message.edit(embed=embed)

    @games.handler
    async def process_game(self, **kwargs):
        session = kwargs.get('session')
        emoji = kwargs.get('emoji')
        grid = session.grid

        # В клетку уже походили
        if not grid.has(emoji):
            return 'ignore'

        state = 'playing'
        players = session.players
        user = kwargs.get('user')

        # Подготовка сессии
        if not session.full():
            state = 'preparing'
            players.append(games.GamePlayer(user, emoji=emojis[len(players)]))
            # Сессия заполнена
            if session.full():
                state = 'playing'

        # Ход может сделать только текущий и сущ в сессии игрок
        player = players.find(user)
        if not player:
            logger.info(f"Player doesnt exist, ignoring...")
            return 'ignore'
        else:
            logger.info(f"Player '{player.user.name}' wanna make a move")
            first_player_abuse = (len(players) == 1 and grid.move_count == 1)
            if not player == players.current or first_player_abuse:
                if first_player_abuse:
                    players.pop()
                logger.info("Not a current player, ignoring...")
                return 'ignore'
        # Убираем кнопку с ячейкой
        await session.message.clear_reaction(emoji)
        # Сдвигаем очередь
        players.pop()
        # Помечаем на поле
        grid.replace(emoji, player.emoji)
        # Игрок сделал выйгрышный ход
        if self.check_for_winner(session):
            players.set_winner(player)
            state = 'won'
        # Все поля помечены, ничья
        elif (grid.move_count == pow(grid.size, 2)):
            state = 'draw'
        return state

    def check_for_winner(self, session: games.GameSession):
        for player in session.players:
            def check_matrix(matrix):
                # По горизонтали
                for x in range(len(matrix)):
                    for y in range(len(matrix[x])):
                        if matrix[x][y]['emoji'] != player.emoji:
                            break
                        elif y == len(matrix) - 1:
                            return player
                # По вертикали
                for x in range(len(matrix)):
                    for y in range(len(matrix[x])):
                        if matrix[y][x]['emoji'] != player.emoji:
                            break
                        elif y == len(matrix) - 1:
                            return player
                # По главной диагонали
                for i in range(len(matrix)):
                    if matrix[i][i]['emoji'] != player.emoji:
                        break
                    elif i == len(matrix) - 1:
                        return player
                # По обратной диагонали
                for x in range(len(matrix)):
                    y = len(matrix)-1-x
                    if matrix[x][y]['emoji'] != player.emoji:
                        break
                    elif x == len(matrix) - 1:
                        return player

            matrix = session.grid.matrix
            if check_matrix(matrix):
                return True

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.manager.remove_session(message.id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed=helper.get_error_embed(desc="Размер поля должен быть целым числом"))
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=helper.get_error_embed(desc="Команда доступна только на серверах"))
        logger.exception(error)


def setup(bot):
    bot.add_cog(TicTacToe(bot))
