FROM kcml2/snl-pytorch:1.4

RUN apt update && apt install libopenmpi-dev git -y

COPY . /agent
WORKDIR /agent
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=support/server
CMD flask run
