FROM debian:stable-slim

RUN groupadd app && useradd -m kekpass -g app

ENV PYTHONUNBUFFERED=1
ENV HOME=/home/kekpass
ENV APP_HOME=/home/kekpass/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . $APP_HOME

RUN chown -R kekpass:app $APP_HOME

USER kekpass
