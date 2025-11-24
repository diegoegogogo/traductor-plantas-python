"""
Script para actualizar 'traductor de plantas.py' para usar el sistema basado en JSON
"""

# Leer el archivo original
with open('traductor de plantas.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Encontrar la línea que dice 'BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = []'
linea_base_datos = None
for i, linea in enumerate(lineas):
    if 'BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = []' in linea:
        linea_base_datos = i
        break

if linea_base_datos is None:
    print("ERROR: No se encontró la línea de BASE_DATOS_PLANTAS")
    exit(1)

print(f"Encontrado BASE_DATOS_PLANTAS en línea {linea_base_datos + 1}")

# Encontrar el cierre de la lista 'plantas = ['
linea_inicio_plantas = None
for i, linea in enumerate(lineas):
    if 'plantas = [' in linea:
        linea_inicio_plantas = i
        break

if linea_inicio_plantas is None:
    print("ERROR: No se encontró 'plantas = ['")
    exit(1)

print(f"Encontrado 'plantas = [' en línea {linea_inicio_plantas + 1}")

# Encontrar el cierre de la lista
contador = 0
linea_cierre_plantas = None
for i in range(linea_inicio_plantas, len(lineas)):
    if '[' in lineas[i]:
        contador += lineas[i].count('[')
    if ']' in lineas[i]:
        contador -= lineas[i].count(']')
    if contador == 0 and i > linea_inicio_plantas:
        linea_cierre_plantas = i
        break

if linea_cierre_plantas is None:
    print("ERROR: No se encontró el cierre de la lista plantas")
    exit(1)

print(f"Cierre de lista en línea {linea_cierre_plantas + 1}")

# Nuevo código para insertar
nuevo_codigo = '''
# Importar el sistema de carga de plantas desde JSON
from planta_config import cargar_plantas as _cargar_plantas_json, PlantaConfig

# Convertir PlantaConfig a ConfiguracionPlanta para compatibilidad
def _convertir_planta_config_a_configuracion(pc: PlantaConfig) -> ConfiguracionPlanta:
    """Convierte PlantaConfig (del JSON) a ConfiguracionPlanta (clase local)."""
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

# Cargar plantas desde JSON y convertir a ConfiguracionPlanta
BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = [
    _convertir_planta_config_a_configuracion(p) for p in _cargar_plantas_json()
]

'''

# Construir el nuevo archivo
nuevas_lineas = (
    lineas[:linea_base_datos] +  # Todo antes de BASE_DATOS_PLANTAS
    [nuevo_codigo] +  # Nuevo código
    lineas[linea_cierre_plantas + 1:]  # Todo después del cierre de la lista plantas
)

# Guardar backup
with open('Traductor de plantas.py.backup', 'w', encoding='utf-8') as f:
    f.writelines(lineas)
print("✓ Backup creado: 'Traductor de plantas.py.backup'")

# Guardar el archivo actualizado
with open('Traductor de plantas.py', 'w', encoding='utf-8') as f:
    f.writelines(nuevas_lineas)

print(f"✓ Archivo actualizado exitosamente")
print(f"  - Líneas eliminadas: {linea_cierre_plantas - linea_base_datos + 1}")
print(f"  - Líneas originales: {len(lineas)}")
print(f"  - Líneas nuevas: {len(nuevas_lineas)}")
print(f"  - Reducción: {len(lineas) - len(nuevas_lineas)} líneas")
