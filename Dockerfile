FROM python:3.11-slim

WORKDIR /app

# تثبيت ffmpeg اللازم لدمج الصوت والفيديو
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean

# تثبيت المكتبات المطلوبة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# تشغيل البوت مع فتح منفذ وهمي لاستقرار السيرفر على Render
CMD python main.py & python3 -m http.server $PORT
