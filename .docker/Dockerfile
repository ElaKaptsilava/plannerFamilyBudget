FROM python:3.12.3-alpine

RUN apk update && \
    apk add --no-cache \
        python3-dev \
        gcc \
        libc-dev \
        libffi-dev

WORKDIR /app

COPY pyproject.toml /app/

COPY poetry.lock /app/

RUN python -m pip install --upgrade pip

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

RUN poetry run python core/manage.py collectstatic --noinput

CMD ["poetry", "run", "python", "core/manage.py", "runserver"]