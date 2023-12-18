FROM python:3.9
LABEL maintainer="bhunesh22"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend_assignment

COPY requirements.txt /backend_assignment/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend_assignment/

EXPOSE 8000