FROM python:3.12-slim

WORKDIR /app

COPY filtrado/ .

RUN pip install --no-cache-dir pymongo

CMD ["python", "filtro.py"]
