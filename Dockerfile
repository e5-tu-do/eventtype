FROM python

RUN apt-get update && apt-get install -y git

RUN pip install django==1.9 gunicorn

COPY ./start.sh /start.sh
RUN chmod +x start.sh
EXPOSE 8000
CMD ["/start.sh"]

