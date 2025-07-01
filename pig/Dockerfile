FROM openjdk:8-jdk

# Instala wget y unzip
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Descarga y descomprime Apache Pig
RUN wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xzf pig-0.17.0.tar.gz && \
    mv pig-0.17.0 /opt/pig && \
    rm pig-0.17.0.tar.gz

# Agrega Pig al PATH
ENV PATH="/opt/pig/bin:${PATH}"

WORKDIR /data

# Copia el script Pig si quieres empaquetarlo dentro
# COPY script.pig /data/script.pig

# Ejecuta el script (opcional si no se sobreescribe con `command`)
CMD ["pig"]
