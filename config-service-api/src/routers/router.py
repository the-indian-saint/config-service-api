from fastapi import APIRouter

from routers.config import router as config_router
from routers.search import router as search_router
from routers.healthcheck import router as healthcheck_router
from routers.index import router as index_router

from settings import settings


api_router = APIRouter()

api_router.include_router(config_router, prefix=settings.prefix, tags=["config"])
api_router.include_router(search_router, prefix=settings.prefix, tags=["search"])
api_router.include_router(healthcheck_router, tags=["health"])
api_router.include_router(index_router, tags=["index"])
