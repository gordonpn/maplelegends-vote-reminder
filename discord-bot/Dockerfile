FROM python:3.10-alpine

RUN adduser \
  --disabled-password \
  --home /home/appuser \
  --shell /bin/bash \
  --system \
  --uid 1000 \
  appuser

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1

RUN apk update && apk add curl gcc python3-dev musl-dev openssl-dev libressl-dev libffi-dev

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app
RUN chown appuser /app
USER appuser

COPY poetry.lock pyproject.toml /app/
COPY . /app

RUN poetry install --no-dev --no-interaction --no-ansi

CMD ["poetry", "run", "python", "/app/discord_bot/app.py"]
