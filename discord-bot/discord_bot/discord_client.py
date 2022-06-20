"""Custom Discord bot
"""
import logging

import discord
from pymongo.collection import Collection

from discord_bot.database import DB


class DiscordClient(discord.Client):
    """Custom Discord client

    Args:
        discord (Client): inherit from Discord client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = DB()
        self.logger = logging.getLogger("discord_bot")

    async def on_ready(self):
        """Callback to signify that the bot is ready"""
        self.logger.info("We have logged in as %s", self.user)

    async def on_message(self, message: discord.Message):
        """Bot reacts to every message posted and has two commands (register and unregister)

        Args:
            message (str): the message object from the event
        """
        if message.author == self.user:
            return

        msg: str = message.content
        if msg.endswith("register") and msg.startswith("$") and len(msg.split(" ")) > 2:
            await message.channel.send(
                "Command has too many arguments, (un)register command only takes 1 argument!"
            )
            return

        username: str = msg.split(" ")[1]
        collection = self.database.get_registered_users()

        if msg.startswith("$register"):
            await self.handle_register(username, collection, message)

        if msg.startswith("$unregister"):
            await self.handle_unregister(username, collection, message)

    async def handle_register(self, username, collection, message):
        """handles the user's intent to register"""
        already_registered = collection.find_one(
            {
                "$and": [
                    {"maplelegends_username": username},
                    {"discord_id": message.author.id},
                ]
            }
        )
        if already_registered is not None:
            await message.channel.send(
                f"Maplelegends username {username} already registered with Discord user {message.author}. Try unregistering."  # noqa: E501 pylint: disable=line-too-long
            )
            return

        result = collection.insert_one(
            document={
                "maplelegends_username": username,
                "discord_id": message.author.id,
            }
        )
        self.logger.debug("Insertion ID: %s", result.inserted_id)
        await message.author.send(
            f"You have registered Maplelegends username: {username}\nYou will start receiving vote reminders."  # noqa: E501 pylint: disable=line-too-long
        )

    async def handle_unregister(self, username, collection: Collection, message):
        """handles the user's intent to unregister"""
        result = collection.delete_many(
            {
                "maplelegends_username": username,
                "discord_id": message.author.id,
            }
        )
        self.logger.debug("Delete acknowledged: %s", result.acknowledged)
        await message.author.send(
            f"You have unregistered Maplelegends username: {username}\nYou will stop receiving vote reminders."  # noqa: E501 pylint: disable=line-too-long
        )
