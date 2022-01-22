# docker build -t nbadviser-slim .
# docker run -d --env-file .env nbadviser-slim
# ---- ENV ----
# NBADVISER_TOKEN
# NBADVISER_CONTROL_CHAT_ID (optional, to get messages on errors in tg)
FROM python:3.8-slim

WORKDIR /usr/src/app
ENV TZ 'Europe/Moscow'

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["python", "-m", "nbadviser"]


