import httpx
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient, ConnectError, ConnectTimeout
from loguru import logger
from starlette.responses import Response, PlainTextResponse

from app.dependencies import get_redis, get_httpx_client
from app.services.target_service import get_next_active_target_service, disable_target_service

router = APIRouter()


@router.api_route("/{path:path}", response_class=PlainTextResponse, methods=["GET", "POST"])
async def balancer(
        path: str, response: Response,
        redis: Redis = Depends(get_redis),
        http_client: AsyncClient = Depends(get_httpx_client)
):

    success = False

    proxy_response = None

    while not success:
        target_service = await get_next_active_target_service(redis)

        if not target_service:
            raise HTTPException(status_code=503)

        try:
            proxy_response = await http_client.get(f"{target_service}{path}")

            success = True
        except (ConnectError, ConnectTimeout):
            logger.info("Failed proxy request. Switch target service")
            await disable_target_service(target_service, redis)

    response.body = proxy_response.content
    response.status_code = proxy_response.status_code

    return response
