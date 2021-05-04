import discord
import logging
import random
import utils.helper as helper
import commands.ext.games as games
import commands.hangman as hangman
from discord.ext import commands

logger = logging.getLogger(__name__)


class HangmanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = games.GameManager(
            states=['ignore', 'new_player', 'launched', 'guessed', 'wrong', 'wrong_ignore', 'lost', 'won'])
        self.themes = hangman.data.themes()

    @commands.check_any(commands.guild_only())
    @commands.group(name="виселица", help="игра", invoke_without_command=True)
    async def execute(self, ctx, theme: str):
        theme = theme.capitalize()
        if not theme in self.themes:
            return await ctx.send(embed=helper.get_error_embed(desc="Данной тематики не существует!"))
        word = hangman.HangmanWord(random.choice(self.themes[theme]))
        session = games.GameSession(
            self.manager, None, 2, 8, 1, theme=theme, word=word, errors=0)
        session.players.append(games.GamePlayer(ctx.author, guesses=0))
        session.message = await ctx.send(embed=self.get_launch_embed(session))
        self.manager.add_session(session)
        await session.message.add_reaction('🚪')

    @execute.command(name="темы")
    async def send_themes(self, ctx):
        description = ""
        for theme, words in self.themes.items():
            description += f"**{theme}**: {len(words)} слов\n"
        await ctx.send(embed=discord.Embed(title="📜 Доступные темы", description=description, colour=discord.Color.blue()))

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

        players = session.players

        if state == 'new_player':
            embed = self.get_launch_embed(session)
            if players.ready():
                await message.add_reaction('▶️')
        elif state == 'launched':
            await message.clear_reactions()
            embed = self.get_guessing_embed(
                "⭐ Матч начался! Чтобы походить, отправьте мне букву", session)
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
        state = await self.process_game_guessing(session=session, user=message.author, content=message.content)
        if state == 'ignore':
            return
        if state == 'guessed' or state == 'wrong' or state == 'wrong_ignore':
            action = 'угадывает ✅' if state == 'guessed' else 'ошибается ❌'
            action = 'выбывает из игры ❌' if state == 'wrong_ignore' else action
            description = f"🤔 {message.author.display_name} выбирает **{message.content.upper()}** и {action}"
            embed = self.get_guessing_embed(description, session)
        elif state == 'lost' or state == 'won':
            description = 'Матч проигран ❌' if state == 'lost' else 'Матч выигран 🎉'
            embed = self.get_ended_embed(description, session)
            embed.colour = discord.Color.red() if state == 'lost' else discord.Color.green()
        await message.delete()
        await reply_message.edit(embed=embed)

    @games.handler
    async def process_game_guessing(self, **kwargs):
        user = kwargs.get('user')
        session = kwargs.get('session')
        players = session.players
        content = kwargs.get('content')

        if not session.launched or (len(content) != 1 and len(content) != len(session.word)):
            return 'ignore'
        if not user == players.current.user:
            return 'ignore'

        player = players.current
        word = session.word
        guesses = word.guess(content) if len(content) == 1 else word.guess_completely(content)
        if guesses > 0:
            player.guesses += guesses
            state = 'guessed'
        else:
            players.pop()
            session.errors += 1
            state = 'wrong'
            # Игрок пытался отгадать целое слово
            if len(content) > 1:
                players.ignore(player)
                state = 'wrong_ignore'
            # Если все игроки в игноре, то автолуз
            if players.lost:
                state = 'lost'
                session.errors = len(hangman.data.hangmans)-1

        if session.errors == len(hangman.data.hangmans)-1 and not word.completed:
            state = 'lost'
        elif word.completed:
            players.set_winner(player)
            state = 'won'
        if state == 'lost' or state == 'won':
            self.manager.remove_session(session.message.id)
        return state

    def get_launch_embed(self, session):
        players = session.players
        description = f"Матч по тематике **{session.theme}**\n\n"

        for player in players:
            description += f"☑️ {player.name}\n"
        if not session.full():
            description += f"\nНажмите 🚪, чтобы присоединиться!\n"
        if players.ready():
            description += f"{players.current.name}, для начала игры нажмите ▶️"
        embed = discord.Embed(
            title="Виселица", description=description, colour=discord.Color.blue())
        return embed

    def get_guessing_embed(self, desc, session):
        description = f"{desc}"
        description += f"{hangman.data.hangmans[session.errors]}\n\n"
        embed = discord.Embed(
            title="Виселица", description=description, colour=discord.Color.blue())
        embed.add_field(name="Текущий ход",
                        value=session.players.current.mention, inline=False)
        if session.word.used:
            embed.add_field(name="Уже использовали", value=", ".join(
                str(letter).upper() for letter in session.word.used))
        embed.add_field(name="Слово",
                        value=session.word.formatted_encrypted, inline=False)
        return embed

    def get_ended_embed(self, desc, session):
        description = f"{desc}\n"
        description += f"{hangman.data.hangmans[session.errors]}\n"
        description += "**Счет:**\n"
        for player in sorted(session.players, key=lambda p: p.guesses, reverse=True):
            description += f"**{player.name}** - {player.guesses}"
            description += " 🏆\n" if player.winner else "\n"
        embed = discord.Embed(
            title="Виселица", description=description, colour=discord.Color.blue())
        embed.add_field(
            name="Слово", value=session.word.formatted_original)
        return embed

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
