FROM python:3.10
WORKDIR /app

RUN printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && \
    apt-get install -y -q curl gnupg2
RUN curl http://nginx.org/keys/nginx_signing.key | apt-key add -

RUN apt-get update
#RUN RUNLEVEL=1 apt-get install -y -q nginx

RUN wget -O init-deb.sh https://www.linode.com/docs/assets/660-init-deb.sh
RUN mv init-deb.sh /etc/init.d/nginx
RUN chmod +x /etc/init.d/nginx
RUN /usr/sbin/update-rc.d -f nginx defaults

RUN mkdir -p /usr/share/nginx/html
COPY ./front-end /usr/share/nginx/html
RUN mkdir /app/front-end
COPY ./front-end ./front-end
RUN pip install gdown
RUN gdown --id 1ASv40otDT8YdSp71D-8zh3XU3EtoEngR

RUN pip install Pillow
RUN pip install fastapi
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install uvicorn
RUN pip install numpy
RUN pip install python-multipart
RUN pip install transformers==4.29.2
RUN pip install tqdm
COPY ./docker-image-files .
EXPOSE 8000 443 80
ENTRYPOINT ["RUNLEVEL=1", "apt-get", "install", "-y", "-q", "nginx", "&&", "cp", "-a", "/app/front-end/.", "/usr/share/nginx/html/", "&&", "nginx", "-g", "daemon off;", "&&", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
