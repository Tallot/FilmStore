FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
RUN apt install sudo
COPY . /root/project
RUN pip3 install -r /root/project/requirements.txt
WORKDIR /root/project/user_app
EXPOSE 5432
RUN systemctl enable postgresql
RUN /etc/init.d/postgresql start && sudo -u postgres createuser --superuser root && sudo -u root createdb users && sudo python3 manage.py db init && sudo python3 manage.py db migrate && sudo python3 manage.py db upgrade
CMD ["sh", "-c", "service postgresql start ; python3 running.py"]

