"""
Ejemplo de uso del nuevo sistema de configuración de plantas basado en JSON

Este ejemplo muestra cómo usar el módulo planta_config.py para:
- Cargar todas las plantas
- Buscar plantas específicas
- Listar nombres disponibles
- Filtrar por tipo
"""

from planta_config import (
    cargar_plantas,
    buscar_planta,
    listar_nombres_plantas,
    obtener_plantas_por_tipo
)

def ejemplo_1_cargar_todas():
    """Ejemplo 1: Cargar todas las plantas"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Cargar todas las plantas")
    print("="*70)

    plantas = cargar_plantas()
    print(f"\nTotal de plantas cargadas: {len(plantas)}")

    # Mostrar las primeras 5
    print("\nPrimeras 5 plantas:")
    for i, planta in enumerate(plantas[:5], 1):
        print(f"  {i}. {planta.nombre} ({planta.tipo})")


def ejemplo_2_buscar_planta():
    """Ejemplo 2: Buscar una planta específica"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Buscar planta específica")
    print("="*70)

    nombre = "Acacia"
    try:
        planta = buscar_planta(nombre)
        print(f"\nPlanta encontrada: {planta.nombre}")
        print(f"  Tipo: {planta.tipo}")
        print(f"  Humedad óptima: {planta.humedad_min:.1f}% - {planta.humedad_max:.1f}%")
        print(f"  Temperatura óptima: {planta.temperatura_min:.1f}°C - {planta.temperatura_max:.1f}°C")
        print(f"  Luz óptima: {planta.luz_min:.1f}% - {planta.luz_max:.1f}%")
        print(f"  Frecuencia de riego: cada {planta.frecuencia_riego_dias} días")
    except ValueError as e:
        print(f"\nError: {e}")


def ejemplo_3_listar_nombres():
    """Ejemplo 3: Listar nombres de plantas"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Listar nombres de plantas")
    print("="*70)

    nombres = listar_nombres_plantas()
    print(f"\nTotal de plantas disponibles: {len(nombres)}")
    print("\nPrimeras 10 plantas (ordenadas alfabéticamente):")
    for i, nombre in enumerate(nombres[:10], 1):
        print(f"  {i:2d}. {nombre}")


def ejemplo_4_filtrar_por_tipo():
    """Ejemplo 4: Filtrar plantas por tipo"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Filtrar por tipo")
    print("="*70)

    # Obtener todos los tipos disponibles
    todas = cargar_plantas()
    tipos = sorted(set(p.tipo for p in todas))

    print(f"\nTipos de plantas disponibles:")
    for tipo in tipos[:10]:  # Mostrar primeros 10 tipos
        plantas_tipo = obtener_plantas_por_tipo(tipo)
        print(f"  - {tipo}: {len(plantas_tipo)} plantas")


def ejemplo_5_estadisticas():
    """Ejemplo 5: Calcular estadísticas"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Estadísticas del catálogo")
    print("="*70)

    plantas = cargar_plantas()

    # Calcular promedios
    humedad_avg = sum(p.humedad_promedio for p in plantas) / len(plantas)
    temp_min_avg = sum(p.temperatura_min for p in plantas) / len(plantas)
    temp_max_avg = sum(p.temperatura_max for p in plantas) / len(plantas)

    print(f"\nEstadísticas generales de {len(plantas)} plantas:")
    print(f"  Humedad promedio: {humedad_avg:.1f}%")
    print(f"  Temperatura mínima promedio: {temp_min_avg:.1f}°C")
    print(f"  Temperatura máxima promedio: {temp_max_avg:.1f}°C")

    # Plantas con mayor frecuencia de riego
    plantas_sedientas = sorted(plantas, key=lambda p: p.frecuencia_riego_dias)[:5]
    print("\nPlantas que necesitan riego más frecuente:")
    for i, p in enumerate(plantas_sedientas, 1):
        print(f"  {i}. {p.nombre}: cada {p.frecuencia_riego_dias} días")

    # Plantas con menor frecuencia de riego
    plantas_autonomas = sorted(plantas, key=lambda p: p.frecuencia_riego_dias, reverse=True)[:5]
    print("\nPlantas más autónomas (menos riego):")
    for i, p in enumerate(plantas_autonomas, 1):
        print(f"  {i}. {p.nombre}: cada {p.frecuencia_riego_dias} días")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "="*70)
    print("EJEMPLOS DE USO: Sistema de Configuración de Plantas")
    print("="*70)

    ejemplo_1_cargar_todas()
    ejemplo_2_buscar_planta()
    ejemplo_3_listar_nombres()
    ejemplo_4_filtrar_por_tipo()
    ejemplo_5_estadisticas()

    print("\n" + "="*70)
    print("FIN DE LOS EJEMPLOS")
    print("="*70)


if __name__ == "__main__":
    main()
