"""Entrypoint for the Discord bot"""
import asyncio
import logging
import os

import discord
from dotenv import load_dotenv

from discord_bot.background_schedule import schedule_periodically
from discord_bot.discord_client import DiscordClient
from discord_bot.jobs import gtop_check

ONE_HOUR = 3600
LOG_LEVEL = logging.INFO if os.getenv("APP_ENV") == "production" else logging.DEBUG
logging.basicConfig(level=LOG_LEVEL)
load_dotenv()

client = DiscordClient(intents=discord.Intents.default())
asyncio.run_coroutine_threadsafe(
    schedule_periodically(ONE_HOUR, gtop_check, client), client.loop
)
client.run(os.getenv("BOT_TOKEN"))
