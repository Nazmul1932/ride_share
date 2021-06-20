FROM python:3.8-slim-buster

RUN mkdir /connection_service
WORKDIR /connection_service

ADD requirements.txt /connection_service/requirements.txt
RUN pip install -r /connection_service/requirements.txt

ADD . /connection_service

EXPOSE 5002

CMD ["python","/connection_service/connection.py"]