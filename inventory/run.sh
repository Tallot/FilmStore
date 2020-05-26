#!/bin/bash

/etc/init.d/nginx start

uwsgi --socket 127.0.0.1:8001 --module inventory.wsgi
