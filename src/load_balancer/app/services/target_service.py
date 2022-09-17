import json
from pathlib import Path
from typing import List

from aioredis import Redis
from httpx import AsyncClient, ConnectError, ConnectTimeout
from loguru import logger

from app.core.settings import settings
from app.dependencies import get_redis

ACTIVE_TARGET_SERVICES_KEY = f"{settings.APP_PREFIX}_active_target_services"
INACTIVE_TARGET_SERVICES_KEY = f"{settings.APP_PREFIX}_inactive_target_services"


async def load_target_services(file_path: Path, redis: Redis):
    with open(file_path, "r", encoding="utf-8") as file:
        target_services_settings = json.load(file)

    await clear_target_services(redis)

    await redis.rpush(ACTIVE_TARGET_SERVICES_KEY, *target_services_settings["services"])


async def get_target_services(type_: str, redis: Redis) -> List[str]:
    return await redis.lrange(f"{settings.APP_PREFIX}_{type_}_target_services", start=0, end=100)


async def clear_target_services(redis: Redis):
    await redis.delete(ACTIVE_TARGET_SERVICES_KEY)
    await redis.delete(INACTIVE_TARGET_SERVICES_KEY)


async def get_next_active_target_service(redis: Redis) -> str:
    target_service = await redis.lpop(ACTIVE_TARGET_SERVICES_KEY)

    if target_service is not None:
        await redis.rpush(ACTIVE_TARGET_SERVICES_KEY, target_service)

    return target_service


async def disable_target_service(target_service: str, redis: Redis):
    await redis.lrem(ACTIVE_TARGET_SERVICES_KEY, 1, target_service)
    await redis.lpush(INACTIVE_TARGET_SERVICES_KEY, target_service)


async def enable_target_service(target_service: str, redis: Redis):
    await redis.lrem(INACTIVE_TARGET_SERVICES_KEY, 1, target_service)
    await redis.lpush(ACTIVE_TARGET_SERVICES_KEY, target_service)


async def check_inactive_target_services():
    redis = await get_redis()
    http_client = AsyncClient()

    inactive_target_services = await get_target_services("inactive", redis)
    for target_service in inactive_target_services:
        try:
            response = await http_client.get(f"{target_service}hello")

            if response.status_code < 500:
                logger.info(f"Target service {target_service} woke up")
                await enable_target_service(target_service, redis)
        except (ConnectError, ConnectTimeout):
            continue

    await http_client.aclose()
