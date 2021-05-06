import logging

from .session import GameSession

from discord.ext import commands

logger = logging.getLogger(__name__)


class GameManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.sessions = {}

    def add_session(self, session) -> GameSession:
        self.sessions[session.message.id] = session
        return session

    def get_session(self, message_id) -> GameSession:
        return self.sessions.get(message_id, None)

    def remove_session(self, message_id) -> None:
        if self.sessions.get(message_id, None):
            logger.info(f"Removing session #{message_id}")
            del self.sessions[message_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # the message to which the reply came
        source_message = getattr(
            getattr(message, 'reference', None), 'cached_message', None)
        if not source_message:
            return
        session = self.get_session(source_message.id)
        if not session:
            return
        await session.update('on_message', session=session,
                       message=message, user=message.author)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        message = reaction.message
        session = self.get_session(message.id)
        if not session:
            return
        await session.update('on_reaction_add', session=session,
                       reaction=reaction, user=user)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        session = self.get_session(message.id)
        if session:
            session.close()

    async def cog_command_error(self, ctx, error):
        logger.exception(error)