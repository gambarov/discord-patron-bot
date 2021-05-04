import asyncio
import discord
import logging
import utils.helper as helper
import commands.ext.games as games
import commands.hangman as hangman
from discord.ext import commands

logger = logging.getLogger(__name__)


class HangmanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = games.GameManager(
            states=['ignore', 'new_player', 'launched', 'guessed', 'wrong', 'lost', 'won'])

    @commands.command(name="виселица", help="виселица!")
    @commands.check_any(commands.guild_only())
    async def execute(self, ctx, theme: str):
        theme = theme.capitalize()
        word = hangman.Word(hangman.data.get_random_word(theme))
        if not word:
            return await ctx.send(embed=helper.get_error_embed(desc="Данной тематики не существует!"))

        description = f"Матч по тематике **{theme}**\n\n"
        description += f"☑️ {ctx.author.display_name}\n\n"
        description += "Нажмите 🚪, чтобы присоединиться!"

        embed = discord.Embed(
            title="Виселица", description=description, colour=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await message.add_reaction('🚪')
        session = self.manager.add_session(
            message, 2, 4, 1, theme=theme, word=word, errors=0)
        session.players.append(games.GamePlayer(
            ctx.author, guesses=0))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        message = reaction.message
        session = self.manager.get_session(message.id)
        # Сообщение - не сессия игры
        if not session:
            return

        state = await self.process_game_launch(session=session, user=user, emoji=reaction.emoji)
        if state == 'ignore':
            return

        embed = discord.Embed(title="Виселица", colour=discord.Color.blue())
        players = session.players
        description = ""

        if state == 'new_player':
            description = f"Матч по тематике **{session.theme}**\n\n"
            # Список игроков
            for player in players:
                description += f"☑️ {player.name}\n"
            description += "\n"
            # Если еще можно присоед
            if not session.full():
                description += f"Нажмите 🚪, чтобы присоединиться!\n"
            # Кол-во и четность игроков устраивает
            if players.ready():
                description += f"{players.current.name}, для начала игры нажмите ▶️\n"
                await message.add_reaction('▶️')
        elif state == 'launched':
            await message.clear_reactions()
            description = f"""
            Матч начался! Чтобы походить, отправьте мне букву
            {hangman.data.hangmans[0]}
            """
            embed.add_field(name="Текущий ход",
                            value=players.current.mention, inline=False)
            embed.add_field(name="Текущее слово",
                            value=session.word.formatted_encrypted, inline=False)
        embed.description = description
        await message.edit(embed=embed)

    @games.handler
    async def process_game_launch(self, **kwargs):
        user = kwargs.get('user')
        session = kwargs.get('session')
        emoji = kwargs.get('emoji')
        players = session.players

        if session.launched:
            return 'ignore'
        if emoji == '🚪' and not session.launched:
            if user in players:
                return 'ignore'
            players.append(games.GamePlayer(user, guesses=0))
            return 'new_player'
        elif emoji == '▶️' and players.ready() and user == players.current.user:
            session.launch()
            return 'launched'
        return 'ignore'

    @commands.Cog.listener()
    async def on_message(self, message):
        # Пытаемся получить сообщение, на который пришел ответ
        reply_message = getattr(
            getattr(message, 'reference', None), 'cached_message', None)
        if not reply_message:
            return
        session = self.manager.get_session(reply_message.id)
        if not session:
            return

        state = await self.process_game_guessing(session=session, user=message.author, letter=message.content)
        if state == 'ignore':
            return

        embed = discord.Embed(
            title="Виселица", description="", colour=discord.Color.blue())
        description = ""

        if state == 'guessed' or state == 'wrong':
            action = 'угадывает ✅' if state == 'guessed' else 'ошибается ❌'
            description = f"""
            🤔 {message.author.display_name} выбирает **{message.content.upper()}** и {action}
            {hangman.data.hangmans[session.errors]}
            """
            embed.add_field(name="Текущий ход",
                            value=session.players.current.mention, inline=False)
            if session.word.used:
                embed.add_field(name="Уже использовали", value=", ".join(str(letter).upper() for letter in session.word.used))
            embed.add_field(name="Текущее слово",
                            value=session.word.formatted_encrypted, inline=False)
        elif state == 'lost' or state == 'won':
            self.manager.remove_session(reply_message.id)
            status = '💀 Матч проигран' if state == 'lost' else '🏆 Матч выигран'
            description = f"""
            {status}!
            {hangman.data.hangmans[session.errors]}
            """
            description += "**Счет:**\n"
            for player in sorted(session.players, key=lambda p: p.guesses, reverse=True):
                description += f"**{player.name}** - {player.guesses}\n"
            embed.add_field(
                name="Слово", value=session.word.formatted_original)
            embed.colour = discord.Color.red() if state == 'lost' else discord.Color.green()
        embed.description = description
        await reply_message.edit(embed=embed)
        await message.delete(delay=1)

    @games.handler
    async def process_game_guessing(self, **kwargs):
        user = kwargs.get('user')
        session = kwargs.get('session')
        players = session.players
        letter = kwargs.get('letter')

        if not session.launched or len(letter) != 1:
            return 'ignore'
        if not user == players.current.user:
            return 'ignore'

        state = ''
        player = players.current
        word = session.word
        if word.guess(letter):
            player.guesses += 1
            state = 'guessed'
        else:
            players.pop()
            session.errors += 1
            state = 'wrong'

        if session.errors == len(hangman.data.hangmans) and not word.completed:
            state = 'lost'
        elif word.completed:
            state = 'won'
        return state

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.manager.remove_session(message.id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=helper.get_error_embed(desc="Укажите тематику"))
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=helper.get_error_embed(desc="Команда доступна только на серверах"))
        logger.exception(error)


def setup(bot):
    bot.add_cog(HangmanCommand(bot))
