"""
Script temporal para extraer la lista de plantas y convertirla a JSON
"""
import json
import sys

# Leer el archivo original
with open('Traductor de plantas.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Encontrar el inicio de la lista
inicio = contenido.find('plantas = [')
if inicio == -1:
    print('ERROR: No se encontró la lista de plantas')
    sys.exit(1)

# Encontrar el final de la lista
contador = 0
pos = inicio + len('plantas = ')
encontrado_inicio = False

for i in range(pos, len(contenido)):
    if contenido[i] == '[':
        if not encontrado_inicio:
            encontrado_inicio = True
        contador += 1
    elif contenido[i] == ']':
        contador -= 1
        if contador == 0:
            fin = i + 1
            break

# Extraer solo la parte de la lista (sin "plantas = ")
lista_str = contenido[inicio + len('plantas = '):fin]

# Evaluar la lista de Python
plantas = eval(lista_str)

print(f"Plantas extraídas: {len(plantas)}")
print(f"Primera planta: {plantas[0]['nombre']}")
print(f"Última planta: {plantas[-1]['nombre']}")

# Guardar como JSON
with open('plantas.json', 'w', encoding='utf-8') as f:
    json.dump(plantas, f, indent=2, ensure_ascii=False)

print(f"\n✓ Archivo 'plantas.json' creado exitosamente con {len(plantas)} plantas")
