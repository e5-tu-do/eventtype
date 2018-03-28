#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:/eventtype/eventtype/

git clone https://github.com/e5-tu-do/eventtype.git

cd eventtype
git checkout dev

python eventtype/manage.py migrate 
# python eventtype/eventtype/manage.py runserver


echo Starting Gunicorn.
exec gunicorn eventtype.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3