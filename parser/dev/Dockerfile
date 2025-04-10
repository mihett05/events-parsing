FROM python:3.11-slim

RUN pip3 install poetry

WORKDIR /app

COPY ../poetry.lock /app/
COPY ../pyproject.toml /app/
RUN poetry install --no-root
COPY ../.. /app

RUN chmod +x ./dev/entrypoint.sh

CMD ["./dev/entrypoint.sh"]