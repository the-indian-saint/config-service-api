import json
from typing import List
import dataclasses
from dataclasses import dataclass, field
from models.config import Config
from settings import settings
from loguru import logger


class ConfigJSONEncoder(json.JSONEncoder):
    """
    JSON encoder for Config objects.
    It extends the default JSONEncoder and provides custom serialization for Config objects.
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class Connector:
    """
    Represents a connector to the database, which stores and retrieves configurations.
    """

    file_path: str
    database: List[Config] = field(default_factory=list)
    cacheValid: bool = True

    def load(self) -> None:
        """
        Loads the database from the file specified in `file_path`.
        Raises FileNotFoundError if the file is not found.
        Raises ValueError if the file has invalid JSON format.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.database = [
                    Config(name=data["name"], metadata=data["metadata"])
                    for data in json.load(file)
                ]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Database file '{self.file_path}' not found."
            ) from None
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON format in database file '{self.file_path}'."
            ) from None

    def save_database(self) -> None:
        """
        Saves the current database to the file specified in `file_path`.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [dict(config) for config in self.database], file, cls=ConfigJSONEncoder
            )

    def clear_cache(self) -> None:
        """
        Clears the cache.
        """
        self.search.cache_clear()

    @logger.catch
    def list_configs(self) -> List[Config] | None:
        """
        Returns a list of all configurations in the database.
        """
        response = [dict(config) for config in self.database]
        if len(response) > 0:
            return response
        return None

    def create_config(self, config: Config) -> tuple[bool, dict]:
        """
        Creates a new configuration and adds it to the database.
        Saves the updated database to the file.
        Returns the created configuration.
        """
        try:
            self.database.append(config)
            self.save_database()
            logger.info(f"Created config {config.name}")
            self.clear_cache()
            return True, dict(config)
        except Exception as e:
            logger.error(f"{e}")
            return False, Config(name="Error", metadata={"Error": "Error"})

    @logger.catch
    def get_config(self, name: str) -> Config:
        """
        Retrieves a configuration by its name from the database.
        Returns the configuration if found, or None if not found.
        """
        for config in self.database:
            if config.name == name:
                return dict(config)
        return None


    def update_config(self, name: str, config: Config) -> tuple[bool, dict]:
        """
        Updates an existing configuration in the database.
        Saves the updated database to the file.
        Returns the updated configuration if found, or None if not found.
        """
        for i, existing_config in enumerate(self.database):
            if existing_config.name == name:
                self.database[i] = config
                self.save_database()
                self.clear_cache()
                logger.info(f"Updated config {config.name}")
                return True, dict(config)
        logger.info(f"Config {name} not found")
        return False, None


    def delete_config(self, name: str) -> tuple[bool, int]:
        """
        Deletes a configuration from the database by its name.
        Saves the updated database to the file.
        """
        counter = 0
        replica = self.database.copy()  # to avoid runtime error
        for i, config in enumerate(replica):
            if config.name == name:
                del self.database[i]
                counter += 1

        self.save_database()
        self.clear_cache()

        logger.info(f"Deleted {counter} configs for {name}")
        if counter > 0:
            return True, counter
        return False, counter

    @logger.catch
    def search(self, query: str) -> List[dict]:
        """
        Searches for configurations in the database that match the given query.
        The query should be in the format "key1.key2.key3...=value".
        Returns a list of matching configurations.
        """
        results = []
        keys, value = query.split("=")[0].split("."), query.split("=")[1]
        logger.debug(f"Searching for {query}")

        def search_helper(data, current_keys):
            if not current_keys:
                return True

            key = current_keys[0]
            if key in data:
                if len(current_keys) == 1:
                    return str(data[key]).lower() == value.lower()
                return search_helper(data[key], current_keys[1:])

            return False

        for config in self.database:
            if search_helper(dict(config), keys):
                results.append(dict(config))

        logger.info(f"Found {len(results)} configs for {query}")
        return results


connector_instance = Connector(settings.database_path)
