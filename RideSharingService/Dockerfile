FROM python:3.8-slim-buster

RUN mkdir /ride_sharing_service
WORKDIR /ride_sharing_service

ADD requirements.txt /ride_sharing_service/requirements.txt
RUN pip install -r /ride_sharing_service/requirements.txt

ADD . /ride_sharing_service

EXPOSE 6001

CMD ["python","/ride_sharing_service/driver_rider.py"]