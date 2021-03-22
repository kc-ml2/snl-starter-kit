FROM https://hub.docker.com/orgs/kcml2/snl-base:v0
#FROM python:3.7

COPY . /agent
RUN pip install -r /agent/requirements.txt

ENV FLASK_APP=/agent/server
CMD python /agent/server.py
