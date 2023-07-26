import uvicorn

from fastapi import FastAPI
from routers.router import api_router

from settings import settings

from monitoring import instrumentator

from loguru import logger

app = FastAPI()


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.title,
        description=settings.description,
        debug=settings.debug,
        contact=settings.contact,
        openapi_tags=settings.tag_metadata,
    )
    application.include_router(api_router)
    instrumentator.instrument(application).expose(
        application, include_in_schema=False, should_gzip=True
    )
    return application


config_service = get_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:config_service",
        host=settings.svc_host,
        port=settings.svc_port,
        reload=settings.reload,
        log_level="info",
    )
    logger.info("Config service shutdown")
