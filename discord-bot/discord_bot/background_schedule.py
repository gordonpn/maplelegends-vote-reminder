"""Helper module to run scheduled tasks in the background """
import asyncio
import logging
import traceback


async def schedule_periodically(interval_in_seconds, periodic_function, *args):
    """Helper method to schedule tasks periodically using asyncio"""
    logger = logging.getLogger("discord_bot")
    while True:
        try:
            await asyncio.gather(
                asyncio.sleep(interval_in_seconds),
                periodic_function(*args),
            )
        except Exception as exception:  # pylint: disable=broad-except
            # Catch all exceptions for now to see what is thrown
            logger.error("Caught an exception:\n%s\n", exception)
            logger.error(traceback.format_exc())
