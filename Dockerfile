# Base image Python 3.11 slim
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# تحديث الحزم وتثبيت Node.js و ffmpeg و curl
RUN apt-get update && \
    apt-get install -y nodejs npm ffmpeg curl && \
    apt-get clean

# نسخ ملف المتطلبات وتثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع
COPY . .

# نقطة الدخول لتشغيل البوت
CMD python main.py & python3 -m http.server $PORT
