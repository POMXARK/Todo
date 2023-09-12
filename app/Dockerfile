# multiple stage build

FROM python:3.10.1 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV DOCKER_BUILDKIT=1
WORKDIR /usr/src/app

FROM base as basic
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM base as build
COPY --from=basic /usr/src/app/requirements.txt /tmp/requirements.txt
RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.36.2' && \
    .venv/bin/pip install -r /tmp/requirements.txt

FROM python:3.10.1-slim as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /usr/src/app/
ENV PATH=/usr/src/app/.venv/bin:$PATH
COPY --from=build /usr/src/app/.venv /usr/src/app/.venv
COPY . /usr/src/app/