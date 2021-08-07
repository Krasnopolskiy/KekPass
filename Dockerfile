FROM debian:stable-slim

RUN groupadd app && useradd -m kekpass -g app

ENV PYTHONUNBUFFERED=1
ENV HOME=/home/kekpass
ENV APP_HOME=/home/kekpass/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN apt update -y && apt upgrade -y
RUN apt install -y python3 python3-pip

RUN apt install -y less
RUN chmod 4111 /usr/bin/less

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . $APP_HOME

ENV FLAG_SSTI=antiflag{d0_n0t_th1nk_1n_p4tt3rn5}
ENV FLAG_RCE=antiflag{tr0et0ch1e}
ENV FLAG_ROOT=antiflag{pr0h1b1t3d_l1t3r4tur3}

RUN echo $FLAG_RCE > $APP_HOME/flag.txt
RUN echo $FLAG_ROOT > /root/flag.txt

RUN chown -R kekpass:app $APP_HOME

USER kekpass
