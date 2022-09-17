from aioredis import Redis
from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse

from app.dependencies import get_redis
from app.services.track import increment_tracking_requests_count

router = APIRouter()


@router.get("/hello", response_class=PlainTextResponse)
async def hello(redis: Redis = Depends(get_redis)):
    await increment_tracking_requests_count(redis)

    return "Hello Black Wall!!!!!!!!!!!"
