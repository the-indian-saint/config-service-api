# Config-Service

The Config-Service is a simple HTTP service that stores and returns configurations that satisfy certain conditions.

## Tech Stack

### Backend

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
  - Fast: It is one of the fastest web frameworks available.
  - Easy: It is easy to use and has a straightforward API.
  - Standards-based: It is based on the open standards for APIs, such as the OpenAPI (formerly known as Swagger) and JSON Schema.
  - Asynchronous: It supports asynchronous programming for efficient handling of concurrent requests.
  - Type hints: It leverages Python's type hinting feature for automatic data validation and API documentation generation.

- Docker: A containerization platform used to package the application and its dependencies into a lightweight, portable container.

- Kubernetes: An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

- Prometheus: A popular open-source monitoring and alerting toolkit. It is used for collecting and storing application metrics.

## Routes

The Config-Service API provides the following routes:

- Index Route

File: `config-service-api/src/routes/index.py`

Method: GET

URL: `/`

Description: This route serves as the index endpoint.

- Config List Route

File: `config-service-api/src/routes/config.py`

Methods:

- GET: Retrieve a list of configurations
- POST: Create a new configuration

URL: `/api/v1/configs`

Description: This route allows you to retrieve a list of configurations and create a new configuration.

- Config Details Route

File: `config-service-api/src/routes/config.py`

Methods:

- GET: Retrieve a specific configuration
- PUT/PATCH: Update a specific configuration
- DELETE: Delete a specific configuration

URL: `/api/v1/configs/{config}`

Description: This route allows you to retrieve, update, and delete a specific configuration.

- Health Check Route

File: `config-service-api/src/routes/healthcheck.py`

Method: GET

URL: `/api/v1/healthcheck`

Description: This route performs a health check of the application.

- Search Route

File: `config-service-api/src/routes/search.py`

Method: GET

URL: `/api/v1/search`

Description: This route allows you to search configurations based on metadata key-value pairs.

- Metrics Route

File: `config-service-api/src/routes/metrics.py`

Method: GET

URL: `/metrics`

Description: This route exposes application metrics in the Prometheus format for scraping.

Please refer to the specific files in the `config-service-api/src/routes` folder for detailed implementation and configuration of each route.

## Models

The Config-Service application includes the following models:

- Config Model

File: `config-service-api/src/models/config.py`

Description: This model represents the configuration entity and defines its structure.

- Health Check Model

File: `config-service-api/src/models/healthcheck.py`

Description: This model represents the health check entity and defines its structure.

Please refer to the specific files in the `config-service-api/src/models` folder for detailed implementation and usage of each model.

## Connector

The Config-Service application includes a connector that performs operations on the JSON database.

- Connector

File: `config-service-api/src/connector/connector.py`

Description: The connector is responsible for interacting with the JSON database and provides methods for CRUD (Create, Read, Update, Delete) operations on the configurations. Additionally, the connector includes a search method that performs a recursive search based on the provided query.

Please refer to the `config-service-api/src/connector/connector.py` file for detailed implementation and usage of the connector.

## Local Development

To start the entire application locally, run the following command:

```bash
make dev
```

## Local Testing

To run the tests locally, use the following command:

```bash
make test
```

Please note that the testing module used is pytest, and the tests reside in the config-service-api/test directory.

Deploy to DockerHub
To deploy the application to DockerHub, execute the following command:

```bash
make docker-push
```

## OPEN API Documentation

```bash
make dev
```

check http://localhost:8000/docs

## Prometheus Monitoring

The Config-Service application integrates with Prometheus for monitoring and collecting metrics. You can scrape the application metrics using the /metrics route. Prometheus provides powerful features for aggregating, visualizing, and alerting on the collected metrics, helping you gain insights into the application's performance and behavior.
