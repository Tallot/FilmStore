FROM python:3.6

RUN mkdir /inventory
WORKDIR /inventory
COPY . /inventory/
RUN pip install -r requirements.txt
RUN apt update
RUN apt -y install nginx
RUN ln -s /inventory/inventory_nginx.conf /etc/nginx/sites-enabled/
EXPOSE 8000
RUN chmod +x ./run.sh
CMD ["./run.sh"]

