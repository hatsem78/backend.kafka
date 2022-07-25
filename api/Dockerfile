FROM python:3.6.8-alpine3.9

ENV PYTHONUNBUFFERED=1


LABEL MAINTAINER="<hatsem78@gmail.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/


ADD . /var/www/

COPY gunicorn_conf.py /gunicorn_conf.py

COPY core/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh


RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www


EXPOSE 8007

CMD ["python3", "main.py"]