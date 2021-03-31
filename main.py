import os, logging.config

from dotenv import load_dotenv
from bot.patron import Patron

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def main():
    logging.config.fileConfig('logs/config.cfg')
    bot = Patron()
    bot.run(TOKEN)

if __name__ == "__main__":
    main()