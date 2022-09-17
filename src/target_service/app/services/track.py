from aioredis import Redis
from loguru import logger

from app.core.settings import settings

TRACKING_REQUESTS_COUNT = f"{settings.APP_PREFIX}_tracking_requests_count"


async def clear_tracking_requests_count(redis: Redis):
    await redis.set(TRACKING_REQUESTS_COUNT, 0)


async def increment_tracking_requests_count(redis: Redis):
    await redis.incr(TRACKING_REQUESTS_COUNT)


async def log_tracking_requests_count(redis: Redis):
    logger.info(
        f"Current requests count: {await redis.get(TRACKING_REQUESTS_COUNT)}"
    )
