FROM python:3.11.0-slim-buster

RUN apk update \
    && apk add --no-cache git openssh-client build-base musl-dev libffi-dev \
    && pip install poetry

RUN mkdir -p /app/src
WORKDIR /app/src
ADD *.py ./
ADD moyashi_ramen_collector ./moyashi_ramen_collector
ADD poetry.lock ./
ADD pyproject.toml ./
ADD bin ./bin
# 仮想環境を作成しない設定
RUN poetry config virtualenvs.create false &&  poetry install  --no-dev


ENTRYPOINT ["python", "run.py"]
