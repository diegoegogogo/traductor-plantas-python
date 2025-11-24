"""
Módulo de configuración de plantas con carga optimizada desde JSON.

Este módulo proporciona:
- PlantaConfig: dataclass para representar la configuración de una planta
- cargar_plantas(): función con cache para cargar todas las plantas
- buscar_planta(): función para buscar una planta por nombre

IMPORTANTE: Esta es la nueva implementación que reemplaza la lista hardcodeada
de plantas en el archivo principal. Usa JSON + cache LRU para cargar rápidamente.
"""

import os
import json
import random
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class PlantaConfig:
    """
    Configuración completa de una planta.

    Esta clase es COMPATIBLE con ConfiguracionPlanta del módulo principal,
    pero incluye campos adicionales para análisis estadístico.
    """
    nombre: str
    tipo: str
    humedad_min: float
    humedad_max: float
    humedad_promedio: float
    humedad_desviacion: float
    temperatura_min: float
    temperatura_max: float
    luz_min: float
    luz_max: float
    umbral_sequia: float
    frecuencia_riego_dias: int


@lru_cache()  # hace la carga MUCHÍSIMO más rápida
def cargar_plantas() -> list[PlantaConfig]:
    """
    Carga todas las plantas desde el archivo plantas.json.

    Returns:
        Lista de objetos PlantaConfig con todas las plantas.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo plantas.json
        json.JSONDecodeError: Si el archivo JSON está malformado
    """
    # 1. Obtenemos dónde está este script (dentro de carpeta src)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # 2. Construimos la ruta subiendo un nivel (..) para salir de src
    # Esto busca el archivo en: Traductor de plantas/data/plantas.json
    ruta_json = os.path.join(directorio_actual, "..", "data", "plantas.json")

    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f) # Cargamos los datos del archivo
            return [PlantaConfig(**planta) for planta in data] # Devuelve los datos (o procesalos aqui)
        
    except FileNotFoundError:
        # Esto se ejecuta si falla el 'open'
        print(f"ERROR: No se encontro el archivo en: {ruta_json}")
        return [] # Devuelve una lista vacia para que no falle lo demas


def buscar_planta(nombre: str) -> PlantaConfig:
    """
    Busca una planta por nombre (case-insensitive).

    Args:
        nombre: Nombre de la planta a buscar.

    Returns:
        PlantaConfig de la planta encontrada.

    Raises:
        ValueError: Si no se encuentra la planta.
    """
    plantas = cargar_plantas()
    for p in plantas:
        if p.nombre.lower() == nombre.lower():
            return p
    raise ValueError(f"No se encontró la planta '{nombre}'.")


def listar_nombres_plantas() -> list[str]:
    """
    Retorna una lista con los nombres de todas las plantas disponibles.

    Returns:
        Lista de nombres de plantas ordenada alfabéticamente.
    """
    plantas = cargar_plantas()
    return sorted([p.nombre for p in plantas])


def obtener_plantas_por_tipo(tipo: str) -> list[PlantaConfig]:
    """
    Obtiene todas las plantas de un tipo específico.

    Args:
        tipo: Tipo de planta a buscar (ej: "Cactus", "Suculenta", etc.)

    Returns:
        Lista de PlantaConfig que coinciden con el tipo.
    """
    plantas = cargar_plantas()
    return [p for p in plantas if p.tipo.lower() == tipo.lower()]
