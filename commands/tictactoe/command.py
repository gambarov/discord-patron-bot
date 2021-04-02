from discord.ext import commands
import discord, logging
from utils.helper import get_discord_color

from commands.tictactoe.manager import GameManager
from commands.tictactoe.grid import GameGrid

logger = logging.getLogger('discord') 

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = GameManager()

    @commands.command(name = "тик", help = "крестики-нолики!")
    async def execute(self, ctx):
        grid = GameGrid()
        embed = discord.Embed(description = str(grid), colour = get_discord_color('info'))
        embed.set_author(name = "Крестики-нолики")
        message = await ctx.send(embed = embed)
        for i in range(len(grid.matrix)):
            for j in range(len(grid.matrix[i])):
                emoji = grid.matrix[i][j]['emoji']
                await message.add_reaction(emoji)
        self.manager.add_session(id = message.id, grid = grid)

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
        player = session.move_current_player(user)
        # Текущий юзер - не текущий игрок
        if not player:
            return
        await message.clear_reaction(reaction.emoji)
        # Получаем тип и эмоджи хода
        player_type = session.get_player_type(player)
        player_emoji = self.manager.get_player_emoji_move(player_type)
        # Помечаем на поле
        grid.set(player_type, player_emoji, reaction.emoji)
        embed = discord.Embed(description = str(grid), colour = get_discord_color('info'))
        embed.set_author(name = "Крестики-нолики")
        first_player = session.get_player('first')
        second_player = session.get_player('second')
        embed.add_field(name = "Игрок №1", value = "Ожидается" if first_player == None else "<@!{}>".format(first_player.id))
        embed.add_field(name = "Игрок №2", value = "Ожидается" if second_player == None else "<@!{}>".format(second_player.id))
        player_winner = self.manager.check_for_winner(session)
        if player_winner:
            embed.add_field(name = "Победитель:", value = "<@!{}>".format(player_winner.id), inline = False)
            embed.colour = get_discord_color('success')
        elif self.manager.check_for_draw(session):
            embed.add_field(name = "Игра завершена", value = "Ничья!", inline = False)
            embed.colour = get_discord_color('warning')
        else:
            player_next = first_player if (second_player == player) else second_player
            if player_next:
                move_emoji = self.manager.get_player_emoji_move(session.get_player_type(player_next))
                embed.add_field(name = "Текущий ход", value = "{} ({})".format("<@!{}>".format(player_next.id), move_emoji), inline = False)
        await message.edit(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        session = self.manager.sessions.get(message.id, None)
        if session:
           self.manager.delete_session(message.id)
           
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed = discord.Embed(description = "Размер поля должен быть целым числом", colour = get_discord_color('error')))
        logger.exception(error)
        await ctx.send(embed = discord.Embed(description = "Неизвестная ошибка!", colour = get_discord_color('error')))

def setup(bot):
    bot.add_cog(TicTacToe(bot))