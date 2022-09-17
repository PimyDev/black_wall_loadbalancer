from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import get_redis
from app.endpoints.balancer import router as balancer_router
from app.services.logger import configure_logger
from app.services.target_service import load_target_services


def register_target_services(fastapi_app: FastAPI):
    @fastapi_app.on_event("startup")
    async def on_startup():
        settings_path = Path(__file__).parent / "target_services.json"

        redis = await get_redis()

        await load_target_services(file_path=settings_path, redis=redis)


def register_openapi(fastapi_app: FastAPI):
    def custom_openapi():
        if fastapi_app.openapi_schema:
            return fastapi_app.openapi_schema
        openapi_schema = get_openapi(
            title="BlackWall-Balancer",
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
    register_target_services(fastapi_app)


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

    fastapi_app.include_router(balancer_router)

    return fastapi_app


app = init_fastapi_app()
