import discord
import os

from .bot_logging import logger
from .config import settings
from discord.ext import commands

TOKEN = settings.BOT_TOKEN
TEST_GUILD_ID = settings.TEST_GUILD_ID

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='!', intents=intents)
        self.test_guild = discord.Object(id=TEST_GUILD_ID)  

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'✅ Loaded: {filename}')
        
        self.tree.copy_global_to(guild=self.test_guild)
        await self.tree.sync()
        logger.info(f'✅ Synced commands to test guild')

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="/help | Version 1.0.0"
        ))
        logger.info(f'✅ Loaded {len(self.cogs)} cogs')
        logger.info(f'✅ 🤖 {self.user} is ready!')
        
bot = Bot()
bot.run(TOKEN, log_handler=None)