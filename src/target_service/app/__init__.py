from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from app.endpoints.hello import router as hello_router


def register_openapi(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="BlackWall-Target",
            version="3.0.0",
            description="",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi


def register_app(app: FastAPI):
    register_cors_middleware(app)
    register_openapi(app)


def register_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def init_app() -> FastAPI:
    app = FastAPI()

    register_app(app)

    app.include_router(hello_router)

    return app

