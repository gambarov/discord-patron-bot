import discord
import logging

import utils.helper as helper

from commands.tictactoe.grid import GameGrid
import commands.ext.games.wrapper as games

from discord.ext import commands

logger = logging.getLogger(__name__)

emojis = ['❌', '⭕']


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = games.GameManager(
            ['preparing', 'playing', 'draw', 'won'])

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
        grid = session.options['grid']

        embed = discord.Embed(
            title="Крестики-нолики", description=str(grid), colour=helper.get_discord_color('info'))

        def add_players_info(embed, session: games.GameSession, about_current: bool):
            players = session.players
            for index, player in enumerate(players):
                embed.add_field(name=f"Игрок #{index+1}",
                                value="<@!{}>".format(player.user.id))
            if about_current and session.ready():
                # Получаем инфу о след игроке
                current = players.current
                if current:
                    embed.add_field(name="Текущий ход", value="{} ({})".format(
                        "<@!{}>".format(current.user.id), current.emoji), inline=False)
            return embed

        players = session.players

        if state == 'preparing':
            # Ход только в существующую клетку
            if not grid.has(reaction.emoji):
                return
            # Юзер уже зарегистрирован
            if players.find(user):
                return
            else:
                # Определяем эмоджи и добавляем игрока
                player_emoji = emojis[len(players)]
                players.append(games.GamePlayer(user, player_emoji))
                # Помечаем на поле
                grid.replace(reaction.emoji, player_emoji)
                embed = add_players_info(embed, session, False)
                embed.description = str(grid)
                if not session.full():
                    embed.set_footer(text="👀 Ожидание игроков...")
                await message.clear_reaction(reaction.emoji)
        elif state == 'playing':
            embed = add_players_info(embed, session, True)
        else:
            # Партия закончена, можно очищать
            self.manager.remove_session(message.id)
            embed = add_players_info(embed, session, False)
            if state == 'won':
                winner = players.winners[0]
                embed.add_field(name="🏆 Победитель:", value="<@!{}>".format(winner.user.id), inline=False)
                embed.colour = helper.get_discord_color('success')
            elif state == 'draw':
                embed.add_field(name="Игра завершена", value="🍻 Ничья!", inline=False)
                embed.colour = helper.get_discord_color('warning')
        await message.edit(embed=embed)

    @games.handler
    async def process_game(self, **kwargs):
        session = kwargs.get('session')

        if not session.full():
            return 'preparing'

        user = kwargs.get('user')
        emoji = kwargs.get('emoji')

        grid = session.options['grid']
        # В клетку уже походили
        if not grid.has(emoji):
            return 'playing'

        player = session.players.find(user)
        if player:
            logger.info(f"Player '{player.user.name}' wanna make a move")
            if not player == session.players.current:
                logger.info("Not a current player, skipping")
                return 'playing'
        # Сдвигаем очередь
        session.players.pop()
        # Убираем кнопку с ячейкой
        await session.message.clear_reaction(emoji)
        # Помечаем на поле
        grid.replace(emoji, player.emoji)
        # Игрок сделал выйгрышный ход
        if self.check_for_winner(session):
            session.players.set_winner(player)
            return 'won'
        # Все поля помечены, ничья
        elif (grid.move_count == pow(grid.size, 2)):
            return 'draw'
        return 'playing'

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

            matrix = session.options['grid'].matrix
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
