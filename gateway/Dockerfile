FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
RUN mkdir /root/project
COPY . /root/project
WORKDIR /root/project/gateway/gateway_app
RUN python3 running.py
