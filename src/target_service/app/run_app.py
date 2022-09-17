from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import get_redis
from app.endpoints.hello import router as hello_router
from app.services.logger import configure_logger
from app.services.track import clear_tracking_requests_count, log_tracking_requests_count


def register_tracker(fastapi_app: FastAPI):
    @fastapi_app.on_event("startup")
    async def on_startup():
        redis = await get_redis()

        await clear_tracking_requests_count(redis)

        scheduler = AsyncIOScheduler(timezone=pytz.UTC)
        scheduler.add_job(
            log_tracking_requests_count, 'interval', seconds=10, next_run_time=datetime.utcnow(), args=(redis,)
        )
        scheduler.start()


def register_openapi(fastapi_app: FastAPI):
    def custom_openapi():
        if fastapi_app.openapi_schema:
            return fastapi_app.openapi_schema
        openapi_schema = get_openapi(
            title="BlackWall-Target",
            version="3.0.0",
            description="",
            routes=fastapi_app.routes,
        )
        fastapi_app.openapi_schema = openapi_schema
        return fastapi_app.openapi_schema

    fastapi_app.openapi = custom_openapi


def register_fastapi_app(fastapi_app: FastAPI):
    register_cors_middleware(fastapi_app)
    register_openapi(fastapi_app)
    register_tracker(fastapi_app)


def register_cors_middleware(fastapi_app: FastAPI):
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def init_fastapi_app() -> FastAPI:
    configure_logger(capture_exceptions=True)

    fastapi_app = FastAPI()

    register_fastapi_app(fastapi_app)

    fastapi_app.include_router(hello_router)

    return fastapi_app


app = init_fastapi_app()
