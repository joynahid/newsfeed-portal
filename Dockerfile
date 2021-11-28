FROM python:3.8-slim as stage

ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=1000
ENV PATH="/scripts:${PATH}"

WORKDIR /code

COPY requirements.txt ./
COPY ./scripts/ /scripts

RUN chmod -R +x /scripts
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
