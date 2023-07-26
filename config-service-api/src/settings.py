import os
import sys
from functools import lru_cache

from loguru import logger


@lru_cache()
class Settings:
    """
    Configuration settings for the service.
    """

    def __init__(self) -> None:
        self.title: str = "Configuration Service"
        """
        The title of the service.
        """

        self.description: str = """
         A simple HTTP service that stores and returns configurations that satisfy certain conditions.
        """
        """
        A description of the service.
        """

        self.contact: dict = {
            "Name": "Your Team Name",
            "Email": "team_email@hellofresh.com",
            "Slackchannel": "#team_slack_channel",
        }
        """
        Contact information for the service.
        """

        self.debug: bool = True
        """
        Flag indicating if debug mode is enabled.
        """

        self.prefix: str = "/api/v1"
        """
        The API prefix for the service.
        """

        self.tag_metadata: list[dict] = [
            {
                "name": "health",
                "description": """ Used for healthcheck""",
            },
            {
                "name": "config",
                "description": """Creates, updates, deletes and retrieves configurations""",
            },
            {
                "name": "search",
                "description": """Returns configurations that satisfy a given query{key1.key2.key3...=value}""",
            },
            {
                "name": "index",
                "description": """Root""",
            },
        ]
        """
        Metadata for the API tags.
        """

    @property
    def database_path(self) -> str:
        """
        The path to the database file.
        Returns:
            str: The database file path.
        """
        db_path = os.environ.get("DATABASE_PATH", None)
        if not db_path:
            logger.warning("DATABASE_PATH environment variable not set, using default")
            return str(os.path.join(os.getcwd(), "connector/db.json"))
        return db_path

    @property
    def svc_port(self) -> int:
        """
        The port on which the service will run. Application startup will fail if the port is not set.
        Returns:
            int: The service port.
        """
        svc_port = os.environ.get("SVC_PORT", None)
        if not svc_port:
            logger.error("SVC_PORT environment variable not set, exiting application")
            sys.exit(1)
        try:
            svc_port = int(svc_port)
            return svc_port
        except ValueError:
            logger.error(
                "SVC_PORT environment variable is not a valid integer, exiting application"
            )
            sys.exit(1)
        return int(svc_port)

    @property
    def svc_host(self) -> str:
        """
        The host on which the service will run.
        Returns:
            str: The service host.
        """
        svc_host = os.environ.get("SVC_HOST", None)
        if not svc_host:
            logger.warning(
                "SVC_HOST environment variable not set, using default: '0.0.0.0'"
            )
            return "0.0.0.0"
        return svc_host

    @property
    def prom_namespace(self) -> str:
        ns = os.environ.get("NAMESPACE", None)
        if not ns:
            logger.warning(
                "NAMESPACE environment variable not set, using default: 'fastapi'"
            )
            return "fastapi"
        return ns

    @property
    def prom_subsystem(self) -> str:
        sub = os.environ.get("SUBSYSTEM", None)
        if not sub:
            logger.warning("SUBSYSTEM environment variable not set, using default: ''")
            return ""
        return sub

    @property
    def reload(self) -> bool:
        """
        Flag indicating if the service should reload on changes.
        Returns:
            bool: The reload flag.
        """
        if self.debug:
            return True
        return False


settings = Settings()
