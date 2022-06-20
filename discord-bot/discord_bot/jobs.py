"""Module contains jobs to be run in the background """
# TODO: implement healthchecks
import datetime as dt
import logging
import os
from datetime import datetime, timezone

import discord
import requests

from discord_bot.database import DB


async def topg_check(client: discord.Client):
    """Checks the maplelegends topg api and sends a message if voting is required"""
    logger = logging.getLogger("discord_bot")
    database = DB()
    logger.info("Waiting for client to be ready...")
    await client.wait_until_ready()
    logger.info("Discord client ready")
    for user in list(database.get_registered_users().find({})):
        username = user["maplelegends_username"]
        logger.info("Checking if user %s can vote on topg yet", username)
        url = f"https://maplelegends.com/api/topg_canvote?name={username}"
        result = requests.get(url).json()
        if result["canvote"]:
            discord_user = await client.fetch_user(user["discord_id"])
            logger.debug("User %s can vote", discord_user)
            await discord_user.send(
                f"Time to vote on TopG!\nhttps://topg.org/maplestory-private-servers/in-605064-{username}"  # noqa: E501 pylint: disable=line-too-long
            )


async def gtop_check(client: discord.Client):
    """Checks if registered users can vote on gtop100 and sends a message if voting is required"""
    logger = logging.getLogger("discord_bot")
    database = DB()
    logger.info("Waiting for client to be ready...")
    await client.wait_until_ready()
    logger.info("Discord client ready")
    for user in list(database.get_registered_users().find({})):
        username = user["maplelegends_username"]
        logger.info("Checking if user %s can vote on gtop100 yet", username)
        doc = database.get_timestamp_collection().find_one(
            {"$query": {"username": username}, "$orderby": {"$natural": -1}}
        )
        today = datetime.now(timezone.utc)
        if doc is None:
            last_vote_timestamp = today - dt.timedelta(2)
        else:
            last_vote_timestamp = doc["timestamp"].last_vote_timestamp.replace(
                tzinfo=timezone.utc
            )
        last_midnight = datetime(
            today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc
        )
        if last_vote_timestamp < last_midnight:
            logger.debug("User %s can vote", username)
            discord_user = await client.fetch_user(user["discord_id"])
            domain = os.getenv("DOMAIN")
            await discord_user.send(
                f"Time to vote on GTop100!\n{domain}/vote/{username}"
            )
