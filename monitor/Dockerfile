# monitor/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY monitor/ .

RUN pip install --no-cache-dir flask flask-socketio eventlet

CMD ["python", "monitor.py"]
