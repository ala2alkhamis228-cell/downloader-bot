FROM python:3.11-slim

WORKDIR /app

# تثبيت الأدوات اللازمة للنظام
RUN apt-get update && \
    apt-get install -y nodejs npm ffmpeg curl && \
    apt-get clean

# تثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات البوت
COPY . .

# تشغيل البوت وفتح منفذ وهمي لاستقرار السيرفر
CMD python main.py & python3 -m http.server $PORT
