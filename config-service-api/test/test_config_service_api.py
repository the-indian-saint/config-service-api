from fastapi.testclient import TestClient
from main import config_service
from settings import settings

import pytest

client = TestClient(config_service)


def test_list_configs(mocker):
    """
    Test for the /configs endpoint to retrieve a list of configurations.
    """
    mocker.patch(
        "connector.connector.Connector.list_configs",
        return_value=[
            {"name": "TestConfig1", "metadata": {"key": "value1"}},
            {"name": "TestConfig2", "metadata": {"key": "value2"}},
        ],
    )

    response = client.get(f"{settings.prefix}/configs")

    assert response.status_code == 200

    expected_data = [
        {"name": "TestConfig1", "metadata": {"key": "value1"}},
        {"name": "TestConfig2", "metadata": {"key": "value2"}},
    ]
    assert response.json() == expected_data


def test_get_config(mocker):
    """
    Test for the /configs/{name} endpoint to retrieve a specific configuration.
    """
    mocker.patch(
        "connector.connector.Connector.get_config",
        return_value={"name": "TestConfig1", "metadata": {"key": "value1"}},
    )

    response = client.get(f"{settings.prefix}/configs/TestConfig1")

    assert response.status_code == 200

    expected_data = {"name": "TestConfig1", "metadata": {"key": "value1"}}
    assert response.json() == expected_data


def test_create_config(mocker):
    """
    Test for the /configs endpoint to create a new configuration.
    """
    mocker.patch(
        "connector.connector.Connector.create_config",
        return_value=(True, {"name": "TestConfig1", "metadata": {"key": "value1"}}),
    )

    response = client.post(
        f"{settings.prefix}/configs",
        json={"name": "TestConfig1", "metadata": {"key": "value1"}},
    )

    assert response.status_code == 201

    expected_data = {"Created": "TestConfig1"}

    assert response.json() == expected_data


def test_update_config(mocker):
    """
    Test for the /configs/{name} endpoint to update a configuration.
    """
    mocker.patch(
        "connector.connector.Connector.update_config",
        return_value=(True, {"name": "TestConfig1", "metadata": {"key": "value1"}}),
    )

    response = client.put(
        f"{settings.prefix}/configs/TestConfig1",
        json={"name": "TestConfig1", "metadata": {"key": "value1"}},
    )

    assert response.status_code == 200

    expected_data = {"Updated": "TestConfig1"}

    assert response.json() == expected_data

    response = client.patch(
        f"{settings.prefix}/configs/TestConfig1",
        json={"name": "TestConfig1", "metadata": {"key": "value1"}},
    )

    assert response.status_code == 200

    expected_data = {"Updated": "TestConfig1"}

    assert response.json() == expected_data


def test_delete_config(mocker):
    """
    Test for the /configs/{name} endpoint to delete a configuration.
    """
    mocker.patch(
        "connector.connector.Connector.delete_config",
        return_value=(True, 1),
    )

    response = client.delete(f"{settings.prefix}/configs/TestConfig1")

    assert response.status_code == 200

    expected_data = {"Deleted": "TestConfig1", "total": "1"}

    assert response.json() == expected_data


def test_search(mocker):
    """
    Test for the /search endpoint to search configurations.
    """
    mocker.patch(
        "connector.connector.Connector.search",
        return_value=[
            {"name": "TestConfig1", "metadata": {"key1": "value1", "key2": "value2"}},
            {"name": "TestConfig2", "metadata": {"key1": "value1", "key2": "value2"}},
        ],
    )

    response = client.get(f"{settings.prefix}/search?query=metadata.key1.key2=value2")

    assert response.status_code == 200

    assert response.json() == [
        {"name": "TestConfig1", "metadata": {"key1": "value1", "key2": "value2"}},
        {"name": "TestConfig2", "metadata": {"key1": "value1", "key2": "value2"}},
    ]


if __name__ == "__main__":
    pytest.main()
