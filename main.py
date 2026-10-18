"""بوت البرودكاست المنفصل — ارفعه على Railway لوحده."""
from __future__ import annotations

import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("broadcast-bot")

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    raise SystemExit("DISCORD_TOKEN مفقود")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("+", "!", ""),
    intents=intents,
    help_command=None,
)


async def _sync_commands():
    """مزامنة فورية لكل سيرفر + عالمية."""
    for guild in list(bot.guilds):
        try:
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info("Guild sync %s: %s commands", guild.name, len(synced))
        except Exception as e:
            logger.warning("Guild sync failed %s: %s", getattr(guild, "id", "?"), e)
    try:
        synced = await bot.tree.sync()
        logger.info("Global sync: %s commands", len(synced))
    except Exception as e:
        logger.warning("Global sync failed: %s", e)


@bot.event
async def on_ready():
    logger.info("Logged in as %s (%s) | guilds=%s", bot.user, bot.user.id, len(bot.guilds))
    await _sync_commands()


@bot.event
async def on_guild_join(guild: discord.Guild):
    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        logger.info("Joined %s — synced %s commands", guild.name, len(synced))
    except Exception as e:
        logger.warning("Join sync failed: %s", e)


async def main():
    async with bot:
        await bot.load_extension("cogs.broadcast_system")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
