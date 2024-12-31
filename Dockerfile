# python : name of image from docker hub
# 3.9-alpine3.13 : tag name
# 3.9 version of python, alpine3.13 lightweight version of Linux
FROM python:3.9-alpine3.13
LABEL maintainer="winatchai.io"

# ENV for define environment variables of Image
# Recommend from python: for printing output from python to console which 
# prevent any delays of messages
ENV PYTHONUNBUFFERED=1

# copy file to we want to create (to tmp directory, deleted after finish)
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# set directry for docker is run command
WORKDIR /app
EXPOSE 8000

# Create variable DEV default false, for testing ($DEV)
# for install dependencies for Linting and Test
# in docker-compose set args: DEV=true for dev mode
ARG DEV=false

# set command to run
# Every RUN it will create a new Image layer for run command
# Images lightweight single line by \ for avoid using RUN 
# Safegard by using virtual env in docker
# Using python environment to avoid maybe conflig from dependencies python image
# any file is temporarily from add in Docker file, remove it for keep light  weight
# add new user with no password into image with root user (Dont run your application using the root user)
# and no create home for most light weight posible and end with name user
# shell if else end with fi &&
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ;\
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Update PATH enviroment variable 
# PATH directories where executable files or run command
# $PATH is automatically create in linux (from WORK  now is app)
# so we append /py/bin/ into app ensure any Python commands is run under virtual environment python
ENV PATH="/py/bin:$PATH"

# [Should be last line]
# Switt root to user after build image done
# avoid full root (after this any code will run by user django-user)
USER django-user