from discord import Intents, Game
from discord.ext import commands
from dotenv import load_dotenv
from utilities import logger, create_db
import os



class WhitelistBot(commands.Bot):
    def __init__(self, command_prefix: str, *, help_command: commands.HelpCommand | None = None, description: str | None = None, intents: Intents, activity: Game) -> None:
        super().__init__(command_prefix, help_command=help_command, description=description, intents=intents, activity=activity)

    async def on_ready(self):
        files = [filename for filename in os.listdir('cogs') if filename.endswith('.py')]
        for filename in files:
            try:
                await self.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename[:-3]}: {e}')
        logger.info(f'Started bot as {self.user.name}')



if __name__ == '__main__':
    load_dotenv()
    create_db()
    TOKEN = os.getenv('TOKEN')
    bot = WhitelistBot(intents=Intents.all(), activity=Game('Skyfactory4'), command_prefix='#', description='whitelisting people on the Skyfactory4 server under "minecraft.pxlcoarl.de"')
    bot.run(token=TOKEN, log_handler=None)