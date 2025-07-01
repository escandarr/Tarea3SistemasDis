# cache_monitor/Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY cache_monitor/ .

RUN pip install --no-cache-dir flask redis

CMD ["python", "cache_monitor.py"]
