# to_elasticsearch/enviar.py

import csv
import requests
import os
import time

CSV_PATH = "salida/eventos_filtrados/part-m-00000"
ES_URL = "http://elasticsearch:9200/eventos_filtrados/_doc"

def leer_eventos_csv():
    eventos = []
    if not os.path.exists(CSV_PATH):
        print(f"[ES] No se encuentra {CSV_PATH}, esperando datos...")
        return eventos

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for fila in reader:
            if len(fila) == 6:
                eventos.append({
                    "uuid": fila[0],
                    "tipo": fila[1],
                    "comuna": fila[2],
                    "calle": fila[3],
                    "fecha": fila[4],
                    "gravedad": int(fila[5])
                })
    return eventos

def enviar_a_elasticsearch(eventos):
    for evento in eventos:
        try:
            res = requests.post(ES_URL, json=evento)
            if res.status_code == 201:
                print(f"[ES] Evento enviado: {evento['uuid']}")
            else:
                print(f"[ES] Error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"[ES] Excepción al enviar: {e}")
        time.sleep(0.05)

def loop_envio():
    enviados = set()
    while True:
        eventos = leer_eventos_csv()
        nuevos = [e for e in eventos if e["uuid"] not in enviados]

        if nuevos:
            print(f"[ES] Enviando {len(nuevos)} nuevos eventos...")
            enviar_a_elasticsearch(nuevos)
            enviados.update(e["uuid"] for e in nuevos)
        else:
            print("[ES] Sin nuevos eventos. Esperando...")

        time.sleep(10)  # Esperar antes de volver a revisar

if __name__ == "__main__":
    loop_envio()
