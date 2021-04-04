from discord.ext import commands
import discord, logging
from utils.helper import get_discord_color, get_error_embed

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

        embed = discord.Embed(title = "Крестики-нолики", description = str(grid), colour = get_discord_color('info'))
        embed.set_footer(text = "⚙️ Подготовка сессии, подождите...")

        message = await ctx.send(embed = embed)

        for i in range(len(grid.matrix)):
            for j in range(len(grid.matrix[i])):
                emoji = grid.matrix[i][j]['emoji']
                await message.add_reaction(emoji)

        embed.set_footer(text = "👀 Ожидание игроков...")
        await message.edit(embed = embed)
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

        embed = discord.Embed(title = "Крестики-нолики", description = str(grid), colour = get_discord_color('info'))

        pfirst = session.get_player('first')
        psecond = session.get_player('second')
        
        embed.add_field(name = "Игрок №1", value = "<@!{}>".format(pfirst.id))
        embed.add_field(name = "Игрок №2", value = "Ожидается" if psecond == None else "<@!{}>".format(psecond.id))

        winner = self.manager.check_for_winner(session)
        if winner:
            embed.add_field(name = "🏆 Победитель:", value = "<@!{}>".format(winner.id), inline = False)
            embed.colour = get_discord_color('success')
        elif self.manager.check_for_draw(session):
            embed.add_field(name = "Игра завершена", value = "🍻 Ничья!", inline = False)
            embed.colour = get_discord_color('warning')
        else:
            pnext = pfirst if (psecond == player) else psecond
            if pnext:
                move_emoji = self.manager.get_player_emoji_move(session.get_player_type(pnext))
                embed.add_field(name = "Текущий ход", value = "{} ({})".format("<@!{}>".format(pnext.id), move_emoji), inline = False)
        await message.edit(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        session = self.manager.sessions.get(message.id, None)
        if session:
           self.manager.delete_session(message.id)
           
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed = get_error_embed(desc = "Размер поля должен быть целым числом"))
        logger.exception(error)
        await ctx.send(embed = get_error_embed(desc = "Неизвестная ошибка!"))

def setup(bot):
    bot.add_cog(TicTacToe(bot))