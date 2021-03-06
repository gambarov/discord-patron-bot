import os, logging, logging.config
from discord.ext.commands import Bot
from utils import files
from config import options, PRIVATE, testers_id
from dotenv import load_dotenv
from commands.ext.games import GameManager

bot = Bot(**options())


def load_extensions(system):
    for file in files.get_py_files(system):
        bot.load_extension('{}.{}'.format(system.replace('/', '.'), file))


if __name__ == "__main__":
    load_dotenv()

    logging.config.fileConfig('logs/config.cfg')

    bot.add_cog(GameManager(bot))
    load_extensions('commands')
    bot.load_extension('commands.exchange.command')
    bot.load_extension('commands.tictactoe.command')
    bot.load_extension('commands.hangman.command')
    bot.load_extension('commands.minesweeper.command')
    
    load_extensions('events')
    bot.load_extension('events.chat.event')


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    if PRIVATE:
        if not message.author.id in testers_id:
            return
    await bot.process_commands(message)


bot.run(os.getenv('DISCORD_TOKEN'))