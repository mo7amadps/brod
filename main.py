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


@bot.event
async def on_ready():
    logger.info("Logged in as %s (%s)", bot.user, bot.user.id)
    try:
        synced = await bot.tree.sync()
        logger.info("Synced %s slash commands", len(synced))
    except Exception as e:
        logger.warning("Sync failed: %s", e)


async def main():
    async with bot:
        await bot.load_extension("cogs.broadcast_system")
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
