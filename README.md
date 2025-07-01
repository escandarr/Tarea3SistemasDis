En este repositorio se encuentran todos los códigos implementados para poder levantar cada uno de los sistemas solicitados en cada entrega 

  Integrantes:
  * Benjamín Escandar
  * Jorge Gallegos
   
# Tarea 1 - Sistema Distribuidos
  ## Stack de tecnologías usado

[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat)](https://www.docker.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white&style=flat)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white&style=flat)](https://redis.io/)

## Instrucciones de uso

En la terminal utilizar los siguientes comandos:

### 1. Para clonar repositorio:
```bash
 git clone https://github.com/escandarr/ProyectoSD2025.git 
```
### 2. Desde la carpeta `ProyectoSD2025`, levantar los contenedores con:

```bash
sudo docker compose up --build
```

### 3. Para ver la cantidad de registros desde la terminal del modulo de almacenamiento (MongoDB) se utiliza los siguientes comandos:

```bash
sudo docker exec -it mongodb mongosh
use waze_db
db.eventos.countDocuments()
```

### 4. Para poder ver la los graficos ir a de cache y trafico, copiar estas URL's en el browser respectivamente:

```bash
http://localhost:7000/
```

```bash
http://localhost:5000/

```
## Parámetros de configuración

* Generador de tráfico (modificables en `generador/generador.py`):

```python
MODO = "poisson"          # Opciones: "poisson" o "normal"
LAMBDA = 5                # Parámetro para distribución Poisson
MEDIA_NORMAL = 1.0        # Media de la distribución Normal
STD_DEV_NORMAL = 0.2      # Desviación estándar de la distribución Normal

MONITOR_URL = "http://monitor:5000/evento"
```

* Redis (configurado en `docker-compose.yml`):

```yaml

redis:
  image: redis:7.2
  container_name: redis
  ports:
    - "6379:6379"

  command: >
    redis-server
    --maxmemory 100mb
    --maxmemory-policy allkeys-lru

  restart: always
```
- Política de cache: `allkeys-lru` `allkeys-lfu`

- Tamaño máximo: `100MB` `50MB`

---
  
# Tarea 2 - Sistema Distribuidos
  ## Stack de tecnologías usado
  [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat)](https://www.docker.com/)
  [![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white&style=flat)](https://www.mongodb.com/)
  [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat)](https://www.python.org/)
  [![Apache Pig](https://img.shields.io/badge/Apache%20Pig-EE2E2E?style=flat&logo=apacherocketmq&logoColor=white)](https://pig.apache.org/)

---

## Nueva estructura de carpetas con los nuevos modulos y ajustes de algunos para la presente tarea

```
proyecto\_wazeTest/
├── almacenamiento/
├── cache\_monitor/
├── generador/              # Esto genera 'eventos\_sin\_filtrar.csv'
├── pig/                    # Esta carpeta de donde estan los scripts 'Pig'
├── salida/                 # Aqui estan los archivos de salida, los que se crearan al momento de ejecucion
├── visualizador/           # Visualización de los datos via web con 'Flask'                 
├── scraper/
├── docker-compose.yml
├── Makefile
└── README.md
```
## Intrucciones de uso
### 1. Generar los eventos base

```bash
cd generador
docker build -t generador .
docker run --rm -v $(pwd)/../salida:/app/salida generador
````

 **Esto genera**: `salida/eventos_sin_filtrar.csv`

---

### 2. Filtrar eventos con Apache Pig

```bash
cd ../pig
docker build -t pig .
docker run --rm -v $(pwd)/../salida:/data pig /opt/pig/bin/pig -x local /data/script.pig
```

 **Esto genera**: `salida/eventos_filtrados/part-m-00000`

---

### 3. Ejecutar análisis y visualización

```bash
make
```

Esto lo que hace es:
*  Limpia resultados anteriores
*  Ejecuta análisis por comuna, tipo y fecha
*  Inicia visualizador Flask

---

### 4. Visualizar en el navegador

Para poder ver los datos, hay que abrir:
```bash
 http://localhost:8000
```
Dentro, se podrá observar:
*  Incidentes por Comuna
*  Incidentes por Tipo
*  Incidentes por Fecha

##  Limpieza
```bash
docker-compose down
make limpiar
```
---
# Tarea 3 - Sistema Distribuidos: Visualización
   ## Stack de tecnologías usado
  [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat)](https://www.docker.com/)
  [![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white&style=flat)](https://www.mongodb.com/)
  [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat)](https://www.python.org/)
  [![Apache Pig](https://img.shields.io/badge/Apache%20Pig-EE2E2E?style=flat&logo=apacherocketmq&logoColor=white)](https://pig.apache.org/)
  [![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?logo=elasticsearch&logoColor=white&style=flat)](https://www.elastic.co/elasticsearch/)
[![Kibana](https://img.shields.io/badge/Kibana-005571?logo=kibana&logoColor=white&style=flat)](https://www.elastic.co/kibana/)

## Nueva estructura de carpetas con los nuevos modulos y ajustes de algunos para la presente tarea
```
hay que añadir esto
```
## Intrucciones de uso
### 1. Visualizacion de datos 
* Ingresar a Kibana `http://localhost:5601` y crear una “Data View” basada en el índice eventos_filtrados.
* Para monitorear el comportamiento del cache, se debe ingresar a `http://localhost:7000`, en base a las mejores metricas obtenidas en la Tarea 1

### 2. Levantar servicios base `MongoDB, Redis, Elasticsearch` y `Kibana`
```bash
sudo docker compose up -d --build mongodb redis elasticsearch kibana
```
### 3. Una vez que esten cargados los modulos anteriores, ejecutar el `scraper` para estraer los eventos desde Waze y luego alamcenarlos en `MongoDB`, hasta que se complete el total de eventos
```bash
sudo docker compose run --rm scraper
```
### 4. Luego se podrecede en el filtrado y normalizacion de los datos. Esto exportará los datos filtrados a un archivo `eventos_sin_filtrar.csv` dentro de `./salida`

```bash
sudo docker compose build filtrado
sudo docker compose run --rm filtrado
```
### 5. Ya con los datos filtrados, se procede en ejecutar los scripts de Pig
```bash
sudo docker compose build pig
sudo docker compose run --rm pig
```

* Dentro de la terminal del contenedor, ejecutar los comandos: 
```bash
pig -x local /data/script.pig
pig -x local /data/comuna.pig
pig -x local /data/tipo.pig
pig -x local /data/fecha.pig
```
* Esto genera los archivos ya procesados `/salida/eventos_filtrados/`; `/salida/salida_pig/comuna/`; `/salida/salida_pig/tipo/`; `/salida/salida_pig/fecha/` 

### 6.  Para enviar los eventos filtrados a Elasticsearch. Esto carga los datos procesados a Elasticsearch `eventos_filtrados`
```bash
sudo docker compose run --rm to_elasticsearch
```

### 7. Luego para ver el flujo de las consultas y activar el modulo de cache
```bash
sudo docker compose up -d  cache_monitor generador
```

Esto hace que:
* El generador consulte eventos desde Elasticsearch.
* `Redis` almacene caché de los eventos consultados.
* El visualizador de caché muestren el comportamiento (hits/misses).



