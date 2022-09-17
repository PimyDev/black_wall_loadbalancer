import asyncio
from contextlib import suppress

from httpx import AsyncClient


async def start_flood():
    http_client = AsyncClient()

    while True:
        with suppress(Exception):
            await http_client.get(f"http://load_balancer/hello")
            await asyncio.sleep(.5)
