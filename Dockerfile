FROM python:3.10
WORKDIR /app

RUN pip install gdown
RUN gdown --id 1ASv40otDT8YdSp71D-8zh3XU3EtoEngR
#RUN mv prefix_only_10_8_10-009.pt /var/lib/data/prefix_only_10_8_10-009.pt
RUN pip install mlflow==2.4.0
RUN pip install psutil
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

ADD start.sh /
RUN chmod +x /start.sh
EXPOSE 8000 443 80 5000
CMD ["/start.sh"]