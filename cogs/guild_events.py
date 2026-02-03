import discord

from bot import settings
from database import insert_settings, remove_settings
from discord.ext import commands

GUILD_LOGS = settings.GUILD_LOGS

class GuildEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            await guild.system_channel.send(
                f'👋 Hi! Thank you for adding me to the server!\n'
                f'🔔 By default, notifications about new giveaways will be sent to this channel, but you can change it using "/setup add".\n\n'
                f'⁉️ A full list of commands can be found using /help.'
            )
            insert_settings({"guild_id": guild.id, "channel_id": guild.system_channel.id})
        else:
            try:
                await guild.owner.send(
                    f'👋 Hi! Thank you for adding me to your server!\n\n'
                    f'Unfortunately, I couldn\'t find a suitable channel for sending notifications about free games, so please use "/setup add" for manual configuration.\n\n'
                    f'A full list of commands can be found using /help.'
                )
            except discord.Forbidden:
                pass

        channel = self.bot.get_channel(GUILD_LOGS)
        if channel:
            embed = discord.Embed(
                title='✅ New server added',
                description=f'**{guild.name}**\nID: {guild.id}\nMembers: {guild.member_count}',
                color=discord.Color.green()
            )
            await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        remove_settings(guild.id)
        channel = self.bot.get_channel(GUILD_LOGS)
        if channel:
            embed = discord.Embed(
                title='❌ Server removed',
                description=f'**{guild.name}**\nID: {guild.id}',
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GuildEvents(bot))