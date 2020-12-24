# pull official base image
FROM python:3.8-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y \
    netcat gettext

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash app
# create the appropriate directories

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

# copy project
COPY --chown=app:app . $APP_HOME

RUN chown app:app $APP_HOME/static $APP_HOME/media

# change to the app user
USER app

RUN python manage.py compilemessages --ignore .pip

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
