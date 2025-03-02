FROM python:3.10
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
EXPOSE 8083
CMD [ "python", "./websocket/server.py" ]