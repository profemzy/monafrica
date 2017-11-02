FROM python:2.7-slim
MAINTAINER Nick Janetakis <nick.janetakis@gmail.com>

RUN apt-get update && apt-get install -qq -y \
        python-pip python-dev uwsgi-plugin-python \
        nginx supervisor build-essential libpq-dev --no-install-recommends

COPY nginx/monafrica.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY monafrica /var/www/app

ENV INSTALL_PATH /monafrica
RUN mkdir -p $INSTALL_PATH
        mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
        && rm /etc/nginx/sites-enabled/default \
        && ln -s /etc/nginx/sites-available/monafrica.conf /etc/nginx/sites-enabled/moafrica.conf \
        && echo "daemon off;" >> /etc/nginx/nginx.conf \
        && chown -R www-data:www-data /var/www/app \
        && chown -R www-data:www-data /var/log

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD ["/usr/bin/supervisord"]
