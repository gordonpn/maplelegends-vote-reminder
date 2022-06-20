FROM python:3.10-alpine as base

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

FROM base as development

ENV FLASK_APP=proxy_server \
  FLASK_RUN_HOST=0.0.0.0 \
  FLASK_ENV=development

EXPOSE 5000
ENTRYPOINT ["poetry", "run"]
CMD ["flask", "run"]

FROM base as production

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=4", "--threads=1", "proxy_server:create_app()"]
