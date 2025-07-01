# filtrado/filtro.py

# Este script se encarga exclusivamente de filtrar, limpiar y exportar los eventos almacenados en MongoDB.
# Su función principal es preparar un archivo CSV con los datos normalizados y consistentes, eliminando registros
# incompletos o inválidos. El resultado será utilizado posteriormente por Apache Pig para el análisis distribuido.
# Separar esta lógica del generador de tráfico permite mantener una arquitectura modular y facilita la reutilización
# del pipeline de procesamiento de datos.

from pymongo import MongoClient
import csv
import os
from datetime import datetime

CSV_SALIDA = "salida/eventos_sin_filtrar.csv"

def exportar_eventos():
    print("[FILTRADO] Exportando eventos desde MongoDB...")
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["waze_db"]
    coleccion = db["eventos"]
    eventos = list(coleccion.find({}))

    if not eventos:
        print("⚠ No hay eventos en la base de datos.")
        return

    headers = ["uuid", "type", "city", "street", "date", "severity"]
    os.makedirs(os.path.dirname(CSV_SALIDA), exist_ok=True)

    with open(CSV_SALIDA, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        # writer.writeheader()  
        for e in eventos:
            writer.writerow({
                "uuid": e.get("uuid", ""),
                "type": str(e.get("type", "")).lower(),
                "city": str(e.get("city", "")).lower(),
                "street": str(e.get("street", "")).lower(),
                "date": datetime.fromtimestamp(e.get("pubMillis", 0) / 1000.0).strftime("%Y-%m-%d %H:%M:%S"),
                "severity": e.get("severity", "")
            })

    print(f"[FILTRADO] Exportación completa: {CSV_SALIDA} ({len(eventos)} eventos)")

if __name__ == "__main__":
    exportar_eventos()
