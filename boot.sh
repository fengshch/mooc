#!/bin/sh

python manage.py db upgrade
python manage.py run &
nginx -g "daemon off;" 

