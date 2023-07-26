from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

from models.config import Config
from connector.connector import connector_instance as connector


router = APIRouter()
connector.load()


@router.get("/configs", response_model=None)
async def list_configs() -> JSONResponse | HTTPException:
    """
    Retrieve a list of all configurations.
    Returns:
        JSONResponse | HTTPException: The response containing the list of configurations
        or an exception if not found.
    Use like this: curl -X GET "http://{service_host}:{service_port}/api/v1/configs"
    -H  "accept: application/json"
    """
    configs = connector.list_configs()
    if configs:
        return JSONResponse(status_code=200, content=configs)
    return HTTPException(status_code=404, detail="No configs found")


@router.post("/configs", response_model=None)
async def create_config(body: Request) -> JSONResponse | HTTPException:
    """
    Create a new configuration.
    Args:
        body (Request): The request body containing the configuration data.
    Returns:
        JSONResponse | HTTPException: The response indicating success or failure of the creation.
    Use like this: curl -X POST "http://{service_host}:{service_port}/api/v1/configs"
        -H  "accept: application/json" \
        -H  "Content-Type: application/json" -d "{\"name\":\"string\",\"metadata\":{\"key\":\"string\"}}"
    """
    config = Config(**await body.json())
    success, _ = connector.create_config(config)
    if success:
        return JSONResponse(status_code=201, content={"Created": f"{config.name}"})
    return HTTPException(status_code=409, detail=f"Unable to update {config.name}")


@router.get("/configs/{name}", response_model=None)
async def get_config(name: str) -> JSONResponse | HTTPException:
    """
    Retrieve a specific configuration by name.
    Args:
        name (str): The name of the configuration to retrieve.
    Returns:
        JSONResponse | HTTPException: The response containing the configuration data
        or an exception if not found.
    Use like this: curl -X GET "http://{service_host}:{service_port}/api/v1/configs/{name}"
         -H  "accept: application/json"
    """
    config = connector.get_config(name)
    if config is not None:
        return JSONResponse(status_code=200, content=config)
    return HTTPException(status_code=404, detail=f"Config {name} not found")


@router.delete("/configs/{name}", response_model=None)
async def delete_config(name: str) -> JSONResponse | HTTPException:
    """
    Delete a configuration by name.
    Args:
        name (str): The name of the configuration to delete.
    Returns:
        JSONResponse | HTTPException: The response indicating success or failure of the deletion.
    Use like this: curl -X DELETE "http://{service_host}:{service_port}/api/v1/configs/{name}"
        -H  "accept: application/json"
    """
    response, count = connector.delete_config(name)
    if response:
        return JSONResponse(
            status_code=200, content={"Deleted": f"{name}", "total": f"{count}"}
        )
    return HTTPException(status_code=404, detail=f"Config {name} not found")


@router.put("/configs/{name}", response_model=None)
@router.patch("/configs/{name}", response_model=None)
async def update_config(name: str, body: Request) -> JSONResponse | HTTPException:
    """
    Update a configuration by name.
    Args:
        name (str): The name of the configuration to update.
        body (Request): The request body containing the updated configuration data.
    Returns:
        JSONResponse | HTTPException: The response indicating success or failure of the update.
    Use like this: curl -X PUT "http://{service_host}:{service_port}/api/v1/configs/{name}"
        -H  "accept: application/json"
    """
    config = Config(**await body.json())
    success, _ = connector.update_config(name, config)
    if success:
        return JSONResponse(status_code=200, content={"Updated": f"{config.name}"})
    return HTTPException(status_code=404, detail=f"Config {name} not found")
