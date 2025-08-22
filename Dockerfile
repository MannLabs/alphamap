# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.10-bookworm

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/alphamapuser" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    alphamapuser

COPY requirements requirements

RUN pip install --no-cache-dir  -r requirements/requirements.txt

COPY alphamap alphamap
COPY MANIFEST.in MANIFEST.in
COPY LICENSE LICENSE
COPY README.md README.md
COPY pyproject.toml pyproject.toml

RUN pip install --no-cache-dir ".[stable,gui-stable]"

ENV PORT=5006
EXPOSE 5006

# to allow other host ports than 5006
ENV BOKEH_ALLOW_WS_ORIGIN=localhost

ENV CONTAINER_DATA_PATH=/app/data/

USER alphamapuser

CMD ["/usr/local/bin/alphamap"]

# build & run:
# docker build --progress=plain -t alphamap .
# DATA_FOLDER=/path/to/local/data
# docker run -p 5006:5006 -v $DATA_FOLDER:/app/data/ -t alphamap
