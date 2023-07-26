from pydantic import BaseModel


class HeartbeatResult(BaseModel):
    """
    Model representing a heartbeat result.
    """

    is_alive: bool


class StatusResult(BaseModel):
    """
    Model representing a status result.
    """

    is_alive: bool
