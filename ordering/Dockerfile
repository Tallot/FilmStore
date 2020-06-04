FROM python:3.8

RUN mkdir /app
WORKDIR /app
COPY . /app/

ENV TZ=Europe/Kiev

RUN pip install -U pip aiohttp requests pytz hazelcast-python-client 
RUN apt-get update && apt-get install -y curl sqlite3 default-jdk
RUN cd app/hazel/bin && ./start.sh

ENTRYPOINT ["python", "app/app.py"]

