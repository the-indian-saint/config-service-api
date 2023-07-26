SHELL = /usr/bin/env bash -o pipefail
#use appropriate docker registry
DOCKER_REGISTRY = "rohanmatkar/config-service"

# Change this port number for local development
# if you are already using port 8080 for something else
SVC_PORT := 8080

IMAGE := config-service

BASE_IMAGE = $(IMAGE)-base
BUILD_NUMBER ?= "0.0.1"

CONTAINER_NAME = $(IMAGE):$(BUILD_NUMBER)

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -f .DS_Store
	rm -f .pytest_cache
	rm -rf .mypy_cache

.PHONY: pylint
pylint:
	pylint --rcfile=pylint.cfg config-service-api/


.PHONY: format
format:
	black config-service-api/

.PHONY: run
run:
	export PYTHONPATH=$(shell pwd)/config-service-api/src; \
	export DATABASE_PATH=$(shell pwd)/config-service-api/src/connector/db.json; \
	export SVC_PORT=8080; \
	python3 config-service-api/src/main.py

.PHONY: docker-build-base
docker-build-base: clean pylint format
	@echo  "Building base docker image.."
	docker build -t $(BASE_IMAGE):local \
		--file Dockerfile.base .

.PHONY: build
build: docker-build-base
	@echo "Building docker image.."
	docker build -t $(CONTAINER_NAME) \
		--build-arg BASE=$(BASE_IMAGE) \
		--build-arg BUILD_NUMBER=$(BUILD_NUMBER) \
		--file Dockerfile .

.PHONY: dev
dev: build
	docker run --rm --publish $(SVC_PORT):8080 $(CONTAINER_NAME)

.PHONY: test
test: clean format pylint
	@echo "Running tests.."
	export PYTHONPATH=$(shell pwd)/config-service-api/src; \
	export DATABASE_PATH=$(shell pwd)/config-service-api/test/resources/test_db.json; \
	export SVC_PORT=8080; \
	pytest -c pytest.ini config-service-api/test


.PHONY: docker-push
docker-push: build
	@echo "Pushing docker image to registry"
	docker tag $(CONTAINER_NAME) $(DOCKER_REGISTRY):$(BUILD_NUMBER)
	docker push $(DOCKER_REGISTRY):$(BUILD_NUMBER)

.PHONY: kubernetes-deploy
kubernetes-deploy:
	sed -e 's/{{BUILD_NUMBER}}/$(BUILD_NUMBER)/g' k8s/deployment.yaml | kubectl --context=$(CLUSTER_CTX) apply -f k8s/

#make sure minikube is running before running this command
.PHONY:deploy-minikube
deploy-minikube: CLUSTER_CTX=minikube
deploy-minikube: kubernetes-deploy
deploy-minikube: 
	minikube service config-service -n config-service --url
