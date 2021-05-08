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
        self.manager = bot.get_cog('GameManager')
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
        session.message = await ctx.send(embed=self.launch_embed(session))
        await session.message.add_reaction('🚪')
        session.add_handler('on_message', self.on_message)
        session.add_handler('on_reaction_add', self.on_reaction_add)
        self.manager.add_session(session)

    @execute.command(name="темы")
    async def send_themes(self, ctx):
        description = ""
        for theme, words in self.themes.items():
            description += f"**{theme}**: {len(words)} слов\n"
        await ctx.send(embed=discord.Embed(title="📜 Доступные темы", description=description, colour=discord.Color.blue()))

    async def on_reaction_add(self, session, reaction, user):
        emoji = reaction.emoji
        players = session.players
        if session.launched:
            return
        if emoji == '🚪' and not session.launched:
            if user in players:
                return
            players.append(games.GamePlayer(user, guesses=0))
            embed = self.launch_embed(session)
            if players.ready:
                await session.message.add_reaction('▶️')
        elif emoji == '▶️' and players.ready and user == players.current.user:
            session.launch()
            await session.message.clear_reactions()
            embed = self.guessing_embed(
                "⭐ Матч начался! Чтобы походить, отправьте мне букву!", session)
        await session.message.edit(embed=embed)

    async def on_message(self, session, message, user):
        players = session.players
        content = message.content
        word = session.word

        if not session.launched or not word.can_guess(content):
            return
        if not user == players.current.user:
            return

        player = players.current
        guesses = word.guess(content) if len(
            content) == 1 else word.guess_completely(content)
        if guesses > 0:
            player.guesses += guesses
        else:
            players.pop()
            session.errors += 1
            # Игрок пытался отгадать целое слово
            if len(content) > 1:
                players.ignore(player)

        if players.lost or (session.errors == len(hangman.data.hangmans)-1 and not word.completed):
            session.close()
            embed = self.ended_embed("Матч проигран... 🤦", False, session)
            embed.colour = discord.Color.red()
        elif word.completed:
            session.close()
            players.set_winner(player)
            embed = self.ended_embed("Матч выигран! ✌️", True, session)
            embed.colour = discord.Color.green()
        elif guesses > 0:
            description = f"{player.mention} выбирает **{content.upper()}** и угадывает ☑️"
            embed = self.guessing_embed(description, session)
        # попытался отгадать слово целиком
        elif player.ignored:
            description = f"{player.mention} выбирает **{content.upper()}** и выбывает из игры ♿"
            embed = self.guessing_embed(description, session)
        else:
            description = f"{player.mention} выбирает **{content.upper()}** и ошибается 🙅‍♂️"
            embed = self.guessing_embed(description, session)
        await message.delete()
        await session.message.edit(embed=embed)

    def launch_embed(self, session):
        players = session.players
        description = f"Матч по тематике **{session.theme}**\n\n"

        for player in players:
            description += f"☑️ {player.name}\n"
        if not session.full:
            description += f"\nНажмите 🚪, чтобы присоединиться!\n"
        if players.ready:
            description += f"{players.current.name}, для начала игры нажмите ▶️"
        embed = discord.Embed(
            title="Виселица", description=description, colour=discord.Color.blue())
        return embed

    def guessing_embed(self, desc, session):
        embed = discord.Embed(
            title="Виселица", description=desc, colour=discord.Color.blue())
        embed.add_field(name="\u200b", value=hangman.data.hangmans[session.errors], inline=False)
        embed.add_field(name="Текущий ход",
                        value=session.players.current.mention, inline=False)
        if session.word.used:
            embed.add_field(name="Уже использовали", value=", ".join(
                str(letter).upper() for letter in session.word.used), inline=False)
        embed.add_field(name="Слово",
                        value=session.word.formatted_encrypted, inline=False)
        return embed

    def ended_embed(self, desc, win, session):
        embed = discord.Embed(
            title="Виселица", description=desc, colour=discord.Color.green() if win else discord.Color.red())
        embed.add_field(name="\u200b", value=hangman.data.happy_hangman if win else hangman.data.hangmans[len(hangman.data.hangmans)-1], inline=False)
        results = ""
        for player in sorted(session.players, key=lambda p: p.guesses, reverse=True):
            results += f"**{player.name}** - {player.guesses}"
            results += " 🏆\n" if player.winner else "\n"
        embed.add_field(name="Счет:", value=results, inline=False)
        embed.add_field(
            name="Слово", value=session.word.formatted_original, inline=False)
        return embed

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=helper.get_error_embed(desc="Укажите тематику"))
        if isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=helper.get_error_embed(desc="Команда доступна только на серверах"))
        logger.exception(error)


def setup(bot):
    bot.add_cog(HangmanCommand(bot))
