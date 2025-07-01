from pymongo import MongoClient
import random

#Conexión a MongoDB, en docker-compose el servicio se llama: 'mongodb'

client = MongoClient("mongodb://mongodb:27017/")  
db = client["waze_db"]
coleccion = db["eventos"]

def insertar_evento(evento):
    """Inserta un solo evento en la colección"""
    coleccion.insert_one(evento)

def insertar_eventos(eventos):
    """Inserta múltiples eventos en la colección"""
    if eventos:
        coleccion.insert_many(eventos)

def contar_eventos_db():
    """Cuenta todos los eventos almacenados"""
    return coleccion.count_documents({})

def buscar_evento(filtro):
    """Busca un evento que cumpla con un filtro"""
    return coleccion.find_one(filtro)

def buscar_eventos_random(cantidad):
    """Devuelve una lista de eventos aleatorios"""
    total = contar_eventos_db()
    if total == 0:
        return []
    skip_values = random.sample(range(total), min(cantidad, total))
    eventos = []

    for skip in skip_values:
        evento = coleccion.find().skip(skip).limit(1).next()
        eventos.append(evento)
    return eventos

def limpiar_eventos():
    """Elimina todos los eventos"""
    coleccion.delete_many({})