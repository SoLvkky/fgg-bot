import discord

from database import get_actual_offers, insert_settings, remove_settings, get_settings
from datetime import datetime, timezone
from discord.ext import commands
from typing import Optional
from services import ping

app_commands = discord.app_commands

async def embeds_create(games):
    result = []

    for i in games:
        match i.get("store"):
            case "Steam":
                store_icon = "https://cdn2.steamgriddb.com/icon/c81e155d85dae5430a8cee6f2242e82c/32/32x32.png"
            case "Epic Games Store":
                store_icon = "https://cdn2.steamgriddb.com/icon/34ffeb359a192eb8174b6854643cc046/32/32x32.png"

        embed = discord.Embed(
            color=0x09914b,
            title="🎮 " + i.get(f"title"),
            url=i.get("link"),
            description=i.get("desc"),
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_thumbnail(url=i.get("poster"))
        embed.set_author(name=i.get("store"), icon_url=store_icon)
        embed.set_footer(text="Some data provided by IGDB | FGG Bot")
        embed.add_field(name="⭐ Rating", value=f"{i.get("rating")} ({i.get("rating_count")} votes)")
        embed.add_field(name="🪙 Regular Price", value=f"${i.get("price")}")
        embed.add_field(name="📅 Release Date", value=i.get("release"))
        embed.add_field(name="🎭 Genres", value="\n".join(i.get("genres")))
        embed.add_field(name="⌛ Offer Expires", value=datetime.fromisoformat(i.get("expiry")).strftime("%d.%m.%Y %H:%M") + " UTC")
        result.append(embed)

    return result if result else None

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check", description="Check current promotions")
    async def check(self, interaction: discord.Interaction):
        res = get_actual_offers()
        embeds = await embeds_create(res)

        await interaction.response.send_message(content="💸 Current free promotions:\n", embeds=embeds)

    setup = app_commands.Group(name="setup", description="Manage notifications")

    @setup.command(name="add", description="Setup notifications channel (1 per server)")
    @app_commands.describe(channel="Preferred channel", role="Role to mention (optional)")
    @app_commands.default_permissions(administrator=True)
    async def setup_add(self, interaction: discord.Interaction, channel: discord.TextChannel, role: Optional[discord.Role]):
        guild_id = interaction.guild.id
        role_id = role.id if role else None
        insert_settings({
            "guild_id": guild_id,
            "channel_id": channel.id,
            "role_id": role_id
        })
        await interaction.response.send_message(f"✅ Added: {channel.mention} {"with" + role.mention if role else ""}", ephemeral=True)

    @setup.command(name="remove", description="Remove notifications from the server")
    @app_commands.default_permissions(administrator=True)
    async def setup_remove(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        remove_settings(guild_id)
        await interaction.response.send_message(f"✅ Notifications Removed", ephemeral=True)

    @setup.command(name="get", description="Get current notifications channel")
    @app_commands.default_permissions(administrator=True)
    async def setup_get(self, interaction: discord.Interaction):
        guild = interaction.guild
        details = get_settings(guild.id)
        if details["channel_id"] and details["role_id"]:
            channel, role = guild.get_channel(details["channel_id"]), guild.get_role(details["role_id"])
            await interaction.response.send_message(f"Current notifications channel: {channel.mention}. Role: {role.mention}", ephemeral=True)
        elif details["channel_id"] and not details["role_id"]:
            channel = guild.get_channel(details["channel_id"])
            await interaction.response.send_message(f"Current notifications channel: {channel.mention}. No role selected", ephemeral=True)
        else:
            await interaction.response.send_message(f"Notification channel not configured. Use /setup add")

    @app_commands.command(name="help", description="Command list")
    async def help_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("**📖 FGG Bot — Help**\n\n"\
        "**Description:**\nWith this bot, you can easily monitor all free promotions on Steam and Epic Games Store.\n\n" \
        "**Commands:**\n\n" \
        "`/setup add` - Setup notifications channel (1 per server)\n" \
        "`/setup remove` - Remove notifications from the server\n" \
        "`/setup get` - Get current notifications channel\n\n" \
        "`/check` - Check current promotions\n" \
        "`/ping` - Check utils statuses\n" \
        "`/help` - Show this menu\n"
        )

    @app_commands.command(name="ping", description="Check utils statuses")
    async def ping_command(self, interaction: discord.Interaction):
        stats = await ping()
        await interaction.response.send_message(
        "**Current API statuses:**\n\n" \
        f"`Steam API: `{'✅' if stats['steam']['status'] else '❌'} | Ping: {stats['steam']['ping']}ms\n" \
        f"`Epic  API: `{'✅' if stats['epic']['status'] else '❌'} | Ping: {stats['epic']['ping']}ms\n" \
        f"`IGDB  API: `{'✅' if stats['igdb']['status'] else '❌'} | Ping: {stats['igdb']['ping']}ms"
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))
