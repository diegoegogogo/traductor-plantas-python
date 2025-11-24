"""
Script para migrar 'Proyecto traductor de plantas.py' al sistema basado en JSON
"""
import sys

# Leer el archivo original
print("Leyendo 'Proyecto traductor de plantas.py'...")
with open('Proyecto traductor de plantas.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# 1. Agregar imports después de "from enum import Enum"
import_nuevo = """
# Importar sistema de configuración de plantas desde JSON
from functools import lru_cache
import json
"""

pos_import = contenido.find("from enum import Enum\n")
if pos_import == -1:
    print("ERROR: No se encontró 'from enum import Enum'")
    sys.exit(1)

pos_insertar_import = pos_import + len("from enum import Enum\n")
contenido = contenido[:pos_insertar_import] + import_nuevo + contenido[pos_insertar_import:]
print("- Imports agregados")

# 2. Buscar la sección a reemplazar
inicio_busqueda = "# ==========================================\n# BASE DE DATOS DE PLANTAS (960 ESPECIES)\n# =========================================="
fin_busqueda = "# ==========================================\n# FUNCIONES DE UTILIDAD PARA BASE DE DATOS"

pos_inicio = contenido.find(inicio_busqueda)
pos_fin = contenido.find(fin_busqueda, pos_inicio)

if pos_inicio == -1:
    print("ERROR: No se encontró el inicio de la sección de plantas")
    sys.exit(1)

if pos_fin == -1:
    print("ERROR: No se encontró el fin de la sección de plantas")
    sys.exit(1)

# Nuevo código de reemplazo
nuevo_codigo = """# ==========================================
# BASE DE DATOS DE PLANTAS (960 ESPECIES)
# ==========================================

@lru_cache()  # hace la carga MUCHÍSIMO más rápida
def cargar_plantas() -> list[PlantaConfig]:
    \"\"\"
    Carga todas las plantas desde el archivo plantas.json usando cache LRU.

    Returns:
        Lista de objetos PlantaConfig con todas las plantas.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo plantas.json
        json.JSONDecodeError: Si el archivo JSON está malformado
    \"\"\"
    with open("plantas.json", "r", encoding="utf-8") as f:
        lista = json.load(f)
        return [PlantaConfig(**planta) for planta in lista]


def buscar_planta(nombre: str) -> PlantaConfig:
    \"\"\"
    Busca una planta por nombre (case-insensitive).

    Args:
        nombre: Nombre de la planta a buscar.

    Returns:
        PlantaConfig de la planta encontrada.

    Raises:
        ValueError: Si no se encuentra la planta.
    \"\"\"
    plantas = cargar_plantas()
    for p in plantas:
        if p.nombre.lower() == nombre.lower():
            return p
    raise ValueError(f"No se encontró la planta '{nombre}'.")


# Cargar plantas desde JSON (con cache automático)
BASE_DATOS_PLANTAS: List[PlantaConfig] = cargar_plantas()

\"\"\"
Base de datos global con 960 especies de plantas pre-configuradas.

Cada entrada contiene los parámetros ambientales óptimos para esa especie,
incluyendo rangos de humedad, temperatura, luz y frecuencia de riego.

NOTA: La lista de plantas ahora se carga desde plantas.json usando cache LRU
para un rendimiento óptimo.

Total: {len(BASE_DATOS_PLANTAS)} plantas
\"\"\"

"""

# Reemplazar
contenido_nuevo = contenido[:pos_inicio] + nuevo_codigo + contenido[pos_fin:]

print(f"- Sección reemplazada")
print(f"  Tamaño antes: {len(contenido)} bytes")
print(f"  Tamaño después: {len(contenido_nuevo)} bytes")
print(f"  Reducción: {len(contenido) - len(contenido_nuevo)} bytes ({(len(contenido) - len(contenido_nuevo)) / 1024:.1f} KB)")

# Crear backup
with open('Proyecto traductor de plantas.py.backup', 'w', encoding='utf-8') as f:
    f.write(contenido)
print("- Backup creado: 'Proyecto traductor de plantas.py.backup'")

# Guardar archivo nuevo
with open('Proyecto traductor de plantas.py', 'w', encoding='utf-8') as f:
    f.write(contenido_nuevo)

print("\nArchivo actualizado exitosamente!")
print(f"- La lista de 960 plantas ahora se carga desde plantas.json")
print(f"- Se usa cache LRU para cargas ultra rápidas")
print(f"- Archivo reducido significativamente")
