"""
Script para aplicar los cambios al archivo 'Traductor de plantas.py'
Reemplaza la lista hardcodeada de plantas con el sistema basado en JSON
"""
import sys

# Leer el archivo original
print("Leyendo archivo original...")
with open('Traductor de plantas.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# 1. Agregar import después de los imports existentes
import_nuevo = "\n# Importar sistema de configuración de plantas desde JSON\nfrom planta_config import cargar_plantas as _cargar_plantas_json, PlantaConfig\n"

# Buscar la línea después de "from enum import Enum"
pos_import = contenido.find("from enum import Enum\n")
if pos_import == -1:
    print("ERROR: No se encontró 'from enum import Enum'")
    sys.exit(1)

pos_insertar_import = pos_import + len("from enum import Enum\n")
contenido = contenido[:pos_insertar_import] + import_nuevo + contenido[pos_insertar_import:]
print("- Import agregado")

# 2. Reemplazar la sección de BASE_DATOS_PLANTAS
inicio_busqueda = 'BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = []'
fin_busqueda = '# ==========================================' + '\n' + '# FUNCIONES DE UTILIDAD PARA BASE DE DATOS'

pos_inicio = contenido.find(inicio_busqueda)
pos_fin = contenido.find(fin_busqueda, pos_inicio)

if pos_inicio == -1:
    print("ERROR: No se encontró 'BASE_DATOS_PLANTAS'")
    sys.exit(1)

if pos_fin == -1:
    print("ERROR: No se encontró '# FUNCIONES DE UTILIDAD PARA BASE DE DATOS'")
    sys.exit(1)

# Código de reemplazo
nuevo_codigo = '''# Función auxiliar para convertir PlantaConfig a ConfiguracionPlanta
def _convertir_planta_config_a_configuracion(pc: PlantaConfig) -> ConfiguracionPlanta:
    """
    Convierte PlantaConfig (del JSON) a ConfiguracionPlanta (clase local).

    Args:
        pc: Objeto PlantaConfig cargado desde JSON

    Returns:
        ConfiguracionPlanta equivalente
    """
    return ConfiguracionPlanta(
        nombre=pc.nombre,
        humedad_min=pc.humedad_min,
        humedad_max=pc.humedad_max,
        temperatura_min=pc.temperatura_min,
        temperatura_max=pc.temperatura_max,
        luz_min=pc.luz_min,
        luz_max=pc.luz_max,
        umbral_sequia=pc.umbral_sequia,
        frecuencia_riego_dias=pc.frecuencia_riego_dias
    )


# Cargar plantas desde JSON usando cache LRU (mucho más rápido)
# NOTA: La lista de 960 plantas ahora se carga desde plantas.json
BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = [
    _convertir_planta_config_a_configuracion(p) for p in _cargar_plantas_json()
]

'''

# Reemplazar
contenido_nuevo = contenido[:pos_inicio] + nuevo_codigo + contenido[pos_fin:]

print(f"- Sección reemplazada")
print(f"  Tamaño antes: {len(contenido)} bytes")
print(f"  Tamaño después: {len(contenido_nuevo)} bytes")
print(f"  Reducción: {len(contenido) - len(contenido_nuevo)} bytes")

# Guardar archivo nuevo
with open('Traductor de plantas.py', 'w', encoding='utf-8') as f:
    f.write(contenido_nuevo)

print("\nArchivo actualizado exitosamente!")
print(f"- La lista de 960 plantas ahora se carga desde plantas.json")
print(f"- Se usa cache LRU para cargas rápidas")
print(f"- Archivo reducido en ~{(len(contenido) - len(contenido_nuevo)) / 1024:.1f} KB")
