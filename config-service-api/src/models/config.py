from typing import Dict, Any
from pydantic import BaseModel


class Config(BaseModel):
    """
    Model representing a configuration.
    """

    name: str
    metadata: Dict[str, Any]
