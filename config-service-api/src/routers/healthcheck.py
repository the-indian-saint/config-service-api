from fastapi import APIRouter

from models.healthcheck import HeartbeatResult, StatusResult

router = APIRouter()


@router.get("/health", response_model=HeartbeatResult, name="healthcheck")
async def get_healthcheck() -> HeartbeatResult:
    """
    Perform a health check.
    Returns:
        HeartbeatResult: The result of the health check.
    Use like this: curl -X GET "http://{service_host}:{service_port}/health" -H  "accept: application/json"
    """
    heartbeat = HeartbeatResult(is_alive=True)
    return heartbeat


@router.get("/ready", response_model=StatusResult, name="readycheck")
async def get_readycheck() -> StatusResult:
    """
    Perform a readiness check.
    Returns:
        StatusResult: The result of the readiness check.
    Use like this: curl -X GET "http://{service_host}:{service_port}/ready" -H  "accept: application/json"
    """
    status = StatusResult(is_alive=True)
    return status


@router.get("/status", response_model=StatusResult, name="statuscheck")
async def get_statuscheck() -> StatusResult:
    """
    Perform a status check.
    Returns:
        StatusResult: The result of the status check.
    Use like this: curl -X GET "http://{service_host}:{service_port}/status" -H  "accept: application/json"
    """
    status = StatusResult(is_alive=True)
    return status
