FROM python:3.10
WORKDIR /app

RUN printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d
RUN apt-get update && \
    apt-get install -y -q curl gnupg2
RUN curl http://nginx.org/keys/nginx_signing.key | apt-key add -

RUN apt-get update && \
	apt-get install -y -q nginx

copy ./front-end/nginx.conf /etc/nginx/nginx.conf
COPY ./front-end /usr/share/nginx/html

ADD ./front-end/start.sh /
RUN chmod +x /start.sh
EXPOSE 8000 443 80 5000
CMD ["/start.sh"]