#FROM https://hub.docker.com/orgs/kcml2/snl-base:v0
FROM python:3.7

RUN apt update && apt install libopenmpi-dev -y

COPY . /agent
RUN pip3 install --upgrade pip
RUN pip3 install -r /agent/requirements.txt

ENV FLASK_APP=/agent/server
CMD python /agent/server.py
