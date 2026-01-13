FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nodejs npm ffmpeg curl && \
    apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python main.py & python3 -m http.server $PORT
