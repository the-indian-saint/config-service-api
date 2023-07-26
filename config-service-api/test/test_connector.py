import json
import os
import pytest
from typing import List
from models.config import Config
from connector.connector import Connector
from settings import settings


@pytest.fixture(scope="session", autouse=True)
def prepare_test_db():
    """
    Fixture to prepare the test_db.json file by clearing its contents.
    This fixture runs once at the beginning of the test session.
    """
    db_path = settings.database_path

    if os.path.exists(db_path):
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    yield


@pytest.fixture
def test_connector():  # pylint: disable=redefined-outer-name
    """
    Fixture for creating a test Connector instance with a temporary database file.
    """
    db_path = settings.database_path

    yield Connector(str(db_path))


def test_create_config(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the create_config method of Connector class.
    """
    test_connector.load()
    config1 = Config(name="TestConfig1", metadata={"key": "value"})
    config2 = Config(name="TestConfig2", metadata={"key": "value"})

    success, created_config = test_connector.create_config(config1)
    success, created_config = test_connector.create_config(config2)

    assert success is True

    assert isinstance(created_config, dict)

    assert test_connector.get_config("TestConfig1") is not None


def test_list_configs(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the list_configs method of Connector class.
    """
    test_connector.load()
    configs = test_connector.list_configs()

    assert isinstance(configs, List)

    assert len(configs) == 2

    for config in configs:
        assert isinstance(config, dict)


def test_get_config(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the get_config method of Connector class.
    """
    test_connector.load()
    config = test_connector.get_config("TestConfig1")
    config2 = test_connector.get_config("NotPresent")
    assert isinstance(config, dict)

    assert config["name"] == "TestConfig1"
    assert config["metadata"] == {"key": "value"}
    assert config2 is None


def test_update_config(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the update_config method of Connector class.
    """
    test_connector.load()
    updated_config = Config(name="TestConfig1", metadata={"key": "new_value"})

    success, updated_config = test_connector.update_config(
        "TestConfig1", updated_config
    )

    assert success is True

    assert isinstance(updated_config, dict)

    assert test_connector.get_config("TestConfig1")["metadata"]["key"] == "new_value"


def test_update_config_not_found(
    test_connector,
):  # pylint: disable=redefined-outer-name
    """
    Test for the case when update_config method is called with a non-existing configuration name.
    """
    test_connector.load()
    updated_config = Config(name="NonExistingConfig", metadata={"key": "value"})

    success, updated_config = test_connector.update_config(
        "NonExistingConfig", updated_config
    )

    assert success is False

    assert updated_config is None


def test_delete_config(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the delete_config method of Connector class.
    """
    test_connector.load()
    success, count = test_connector.delete_config("TestConfig1")

    assert success is True

    assert count == 1

    assert test_connector.get_config("TestConfig1") is None


def test_delete_config_not_found(
    test_connector,
):  # pylint: disable=redefined-outer-name
    """
    Test for the case when delete_config method is called with a non-existing configuration name.
    """
    test_connector.load()
    success, count = test_connector.delete_config("NonExistingConfig")

    assert success is False

    assert count == 0


def test_search_config(test_connector):  # pylint: disable=redefined-outer-name
    """
    Test for the search method of Connector class.
    """
    test_connector.load()
    results = test_connector.search("metadata.key=value")

    assert isinstance(results, List)

    assert len(results) == 1

    for config in results:
        assert isinstance(config, dict)


def test_search_config_not_found(
    test_connector,
):  # pylint: disable=redefined-outer-name
    """
    Test for the case when search method is called with a query that does not match any configurations.
    """
    test_connector.load()

    results = test_connector.search("metadata.key=nonexistent")

    assert isinstance(results, List)
    assert len(results) == 0
