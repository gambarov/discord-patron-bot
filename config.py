import os, discord
from dotenv import load_dotenv
load_dotenv()

PRIVATE = os.getenv('PRIVATE_MODE', 'FALSE') == 'TRUE'

intents = discord.Intents().all()

def options():
    if PRIVATE:
        return { 'command_prefix':'_', 'intents':intents }
    return { 'command_prefix':('!'), 'intents':intents, 'help_command':None }

testers_id = [ 627833817708625931, 528305867150589970 ]