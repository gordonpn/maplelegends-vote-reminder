"""Helper module to run scheduled tasks in the background """
import asyncio


async def schedule_periodically(interval_in_seconds, periodic_function, *args):
    """Helper method to schedule tasks periodically using asyncio"""
    while True:
        await asyncio.gather(
            asyncio.sleep(interval_in_seconds),
            periodic_function(*args),
        )
