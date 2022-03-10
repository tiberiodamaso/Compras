# syntax=docker/dockerfile:1

FROM python:3.10.2-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN pip install pip --upgrade
RUN apt-get install -y locales
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt


COPY . .

ENTRYPOINT ["sh", "/entrypoint.sh"]