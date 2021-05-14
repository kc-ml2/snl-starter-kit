FROM kcml2/snl-torch:1.4

COPY . /agent
WORKDIR /agent
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=support/server
CMD flask run --host 0.0.0.0