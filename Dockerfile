FROM python:3.8-slim-buster
ARG DEBIAN_FRONTEND=noninteractive

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/drf
WORKDIR /opt/drf

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh && \
    ./entrypoint.sh

EXPOSE 8000

CMD ["python3", "/opt/drf/drf/manage.py", "runserver", "0.0.0.0:8000"]
