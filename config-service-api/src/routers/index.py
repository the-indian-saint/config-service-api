from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
async def root() -> PlainTextResponse:
    """
    Root endpoint of the HelloFresh config Service.
    Returns:
        PlainTextResponse: A plain text response with a welcome message.
    Use like this: curl -X GET "http://{service_host}:{service_port}/" -H  "accept: application/json"
    """
    return PlainTextResponse("Welcome to HelloFresh config Service")
