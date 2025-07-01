# scraper/Dockerfile

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdbus-1-3 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libasound2 libxshmfence1 libpangocairo-1.0-0 libpango-1.0-0 \
    fonts-liberation libappindicator3-1 libxss1 lsb-release

WORKDIR /app

# Copiar la carpeta almacenamiento al contenedor
COPY almacenamiento/ ./almacenamiento/

# Copiar el contenido de scraper
COPY scraper/ .

RUN pip install --no-cache-dir playwright pymongo
RUN playwright install chromium

CMD ["python", "main.py"]
