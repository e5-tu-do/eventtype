#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:/eventtype/eventtype/

git clone https://github.com/e5-tu-do/eventtype.git

python eventtype/eventtype/manage.py migrate 
# python eventtype/eventtype/manage.py runserver

echo $(ls -l)
RUN cd eventtype
echo $(ls -l)


echo Starting Gunicorn.
exec gunicorn eventtype.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3