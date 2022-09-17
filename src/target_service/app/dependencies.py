import aioredis
from aioredis import Redis
from httpx import AsyncClient

from app.core.settings import settings


async def get_redis() -> Redis:
    return await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        decode_responses=True
    )

