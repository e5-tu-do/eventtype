#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:/eventtype/eventtype/

git clone https://github.com/e5-tu-do/eventtype.git
cd eventtype

git checkout for_cloud

python eventtype/manage.py migrate 


echo Starting Gunicorn.
exec gunicorn eventtype.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3