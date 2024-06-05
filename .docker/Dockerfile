FROM python:3.12.3-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

COPY ../pyproject.toml /app


RUN pip3 install poetry

RUN poetry install

COPY . /app

CMD ["poetry", "run", "python", "core/manage.py", "runserver"]
