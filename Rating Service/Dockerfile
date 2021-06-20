FROM python:3.8-slim-buster

RUN mkdir /rating_service
WORKDIR /rating_service

ADD requirements.txt /rating_service/requirements.txt
RUN pip install -r /rating_service/requirements.txt

ADD . /rating_service

EXPOSE 7000

CMD ["python","/rating_service/db.py"]