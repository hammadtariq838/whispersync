FROM python:3.9
RUN apt-get update && apt-get install -y ffmpeg
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt