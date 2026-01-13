FROM python:3.11-slim

WORKDIR /app

# تثبيت الأدوات الضرورية
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean

# تثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# السطر السحري: تشغيل البوت وفي نفس الوقت فتح سيرفر ويب بسيط على المنفذ اللي بيطلبه Render
CMD python main.py & python3 -m http.server $PORT
