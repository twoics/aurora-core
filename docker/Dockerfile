FROM python:3.11.6
RUN apt-get update && apt-get install netcat-traditional -y && apt-get autoremove -y && apt-get clean

WORKDIR /opt
COPY ./pyproject.toml ./poetry.lock* /opt/
COPY ./app/  /opt/app/
COPY ./docker/  /opt/docker/

RUN mkdir -p /opt/logs && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
WORKDIR /opt/app
