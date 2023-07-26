from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from connector.connector import connector_instance as connector

router = APIRouter()
connector.load()


@router.get("/search/", response_model=None)
async def search(query: str = None) -> JSONResponse | HTTPException:
    """
    Search for configurations based on a query string.
    Args:
        query (str, optional): The query string to search for configurations{key1.key2.key3..=value}. Defaults to None.
    Returns:
        JSONResponse | HTTPException: The response containing the search results or an exception if not found.
    Use like this: curl -X GET "http://{service_host}:{service_port}/search/?query={key1.key2.key3=value}"  \
    -H  "accept: application/json"
    """
    if query is not None:
        configs = connector.search(query)
        if configs:
            return JSONResponse(status_code=200, content=configs)
        return HTTPException(status_code=404, detail="No Config Found")
    return HTTPException(status_code=400, detail="Invalid Query")
