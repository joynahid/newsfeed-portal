FROM python:3.8-slim as stage

ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

WORKDIR /code

COPY requirements.txt ./
COPY ./scripts/ /scripts

RUN chmod -R +x /scripts
RUN install.sh

COPY . .

CMD [ "entrypoint.sh" ]