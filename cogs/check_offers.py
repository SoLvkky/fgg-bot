import asyncio
import datetime
import discord

from bot import logger
from cogs import embeds_create
from database import get_settings
from discord.ext import commands, tasks
from utils import check_games

class Monitor(commands.Cog):
    times = [datetime.time(hour=h, minute=31) for h in range(0, 24, 1)]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = 1421545763699298496
        self.check_offers.start()
    
    def cog_unload(self):
        self.check_offers.cancel()
    
    @tasks.loop(time=times)
    async def check_offers(self):
        res = await check_games()
        if not res:
            return
        
        send_tasks = []
        embeds = await embeds_create(res)
        guilds = get_settings()            
        for guild_settings in guilds:
            channel_id = guild_settings.get("channel_id")
            if not channel_id:
                continue
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.warning(f"Channel {channel_id} not found, skipping")
                continue

            role_id = guild_settings.get("role_id")
            content = f"<@&{role_id}> New free promotion(s)!" if role_id else "New free promotion(s)!"

            send_tasks.append(
                self._send_offer(channel, embeds, content, guild_settings.get("guild_id"))
            )

        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)

    async def _send_offer(self, channel, embeds, content, guild_id):
        try:
            await channel.send(content=content, embeds=embeds)
            logger.info(f"Sent offer to guild {guild_id}, channel {channel.id}")
        except discord.Forbidden:
            logger.warning(f"No permissions to send in channel {channel.id}")
        except discord.HTTPException as e:
            logger.error(f"HTTP error sending to {channel.id}: {e}")

    @check_offers.before_loop
    async def before_check_offers(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(Monitor(bot))