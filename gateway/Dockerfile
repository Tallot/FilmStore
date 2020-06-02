FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /root/project
RUN pip3 install -r /root/project/requirements.txt
WORKDIR /root/project/gateway_app
CMD ["python3", "running.py"]
