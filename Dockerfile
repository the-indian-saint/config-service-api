ARG BASE
FROM ${BASE}:local

COPY config-service-api/src ./src

ENV DATABASE_PATH /home/docker-user/hellofresh/config-service/src/connector/db.json
ENV SVC_PORT 8080

EXPOSE 8080

# To make sure we have a process tree that
# allows us to receive stop/shutdown signals
CMD ["python3", "./src/main.py"]