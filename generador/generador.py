# generador.py
# -----------------------------------------------
# Este módulo simula consultas al sistema en base a eventos viales.
# Consulta eventos directamente desde Elasticsearch usando puntuación aleatoria.
# Luego, intenta responder desde Redis (caché) para medir HIT/MISS y simular latencias.
# Reporta cada consulta al monitor de tráfico (monitor.py).
# Este generador cumple el rol de simular usuarios consultando un sistema optimizado con caché.
# -----------------------------------------------

import time
import random
import numpy as np
import requests
import redis
import json

# Conexión a Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Parámetros
MODO = "poisson"  # Puede cambiarse a "normal" si se desea otro patrón
LAMBDA = 5
MEDIA_NORMAL = 1.0
STD_DEV_NORMAL = 0.2
MONITOR_URL = "http://monitor:5000/evento"
ELASTIC_URL = "http://elasticsearch:9200/eventos_filtrados/_search"

def buscar_eventos_elasticsearch(cantidad=1):
    """Consulta eventos aleatorios desde Elasticsearch usando random_score"""
    try:
        query = {
            "size": cantidad,
            "query": {
                "function_score": {
                    "query": { "match_all": {} },
                    "random_score": {}  # Random para simular variedad
                }
            }
        }
        res = requests.get(ELASTIC_URL, json=query)
        if res.status_code == 200:
            resultados = res.json()["hits"]["hits"]
            return [hit["_source"] for hit in resultados]
        else:
            print(f"[ERROR] Fallo en búsqueda ES: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[ERROR] Consulta a Elasticsearch fallida: {e}")
    return []

def enviar_eventos(eventos):
    """Simula la consulta de eventos y gestiona el uso de caché"""
    for evento in eventos:
        evento_id = evento.get("uuid", "desconocido")
        print(f"[GENERADOR] Evento simulado: {evento_id} | Tipo: {evento.get('tipo', 'unknown')}")

        try:
            # 1. Intenta leer desde Redis
            if r.exists(evento_id):
                r.incr("hits")
                print(f"[CACHE] HIT {evento_id}")
            else:
                r.incr("misses")
                r.set(evento_id, json.dumps(evento), ex=3600)  # Guardar en caché por 1h
                print(f"[CACHE] MISS {evento_id}")

            # 2. Notifica al monitor
            requests.post(MONITOR_URL, timeout=0.5)

        except Exception as e:
            print(f"[ERROR] al enviar evento: {e}")

def generador_normal():
    while True:
        delay = np.random.normal(MEDIA_NORMAL, STD_DEV_NORMAL)
        delay = max(0.01, delay)
        eventos = buscar_eventos_elasticsearch(1)
        enviar_eventos(eventos)
        time.sleep(delay)

def generador_poisson():
    while True:
        n_eventos = np.random.poisson(LAMBDA)
        if n_eventos > 0:
            eventos = buscar_eventos_elasticsearch(n_eventos)
            enviar_eventos(eventos)
        time.sleep(1)

def main():
    print(f"[GENERADOR] Iniciando simulación en modo: {MODO}")
    if MODO == "poisson":
        generador_poisson()
    elif MODO == "normal":
        generador_normal()
    else:
        print("[ERROR] Modo inválido.")

if __name__ == "__main__":
    main()
