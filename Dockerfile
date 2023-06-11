FROM python:3.11.1-alpine3.17

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ENV PYTHONPATH=/app

ARG DEV=false
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  apk add --update --no-cache --virtual .tmp-build-deps \
  gcc \
  linux-headers \
  python3-dev \
  musl-dev \
  postgresql-dev && \
  apk add --no-cache postgresql-libs && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ $DEV = "true" ]; \
  then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  apk del .tmp-build-deps && \
  rm -rf /tmp && \
  chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

CMD ["run.sh"]
