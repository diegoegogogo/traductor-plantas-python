"""
Script para generar dashboard con datos REALES de plantas
Lee los datos desde dataset_plantas_960.csv
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from dashboard_plantas import generar_dashboard
from planta_config import buscar_planta

def generar_dashboard_datos_reales(nombre_planta: str, guardar: bool = False):
    """
    Genera un dashboard usando los datos REALES del CSV dataset_plantas_960.csv

    Args:
        nombre_planta: Nombre de la planta (ej: "Acacia", "Aaron's Beard")
        guardar: Si True, guarda la imagen en lugar de mostrarla
    """
    # Ruta al CSV de datos reales
    archivo_csv = os.path.join(os.path.dirname(__file__), 'data', 'dataset_plantas_960.csv')

    print(f"\n{'='*80}")
    print(f"DASHBOARD CON DATOS REALES - {nombre_planta}")
    print(f"{'='*80}\n")

    # Leer CSV con datos reales
    print(f"Leyendo datos desde: {archivo_csv}")
    df = pd.read_csv(archivo_csv)

    # Filtrar datos de la planta específica
    planta_data = df[df['planta'] == nombre_planta]

    if planta_data.empty:
        print(f"\nERROR: Planta '{nombre_planta}' no encontrada en el dataset")
        print(f"\nPlantas disponibles (primeras 10):")
        plantas_disponibles = df['planta'].unique()[:10]
        for i, p in enumerate(plantas_disponibles, 1):
            print(f"  {i}. {p}")
        print(f"\n  ... y {len(df['planta'].unique()) - 10} mas")
        return

    # Extraer datos reales de humedad
    datos_humedad = (planta_data['humedad_pct'].values).tolist()
    dias = len(datos_humedad)

    print(f"OK Planta encontrada: {nombre_planta}")
    print(f"OK Dias de datos reales: {dias}")
    print(f"OK Rango de humedad: {min(datos_humedad):.2f}% - {max(datos_humedad):.2f}%")

    # Obtener configuración de la planta desde plantas.json
    try:
        planta_config = buscar_planta(nombre_planta)

        # Generar datos realistas de temperatura y luz basados en la config
        temp_promedio = (planta_config.temperatura_min + planta_config.temperatura_max) / 2
        temp_rango = (planta_config.temperatura_max - planta_config.temperatura_min) / 2

        luz_promedio = (planta_config.luz_min + planta_config.luz_max) / 2
        luz_rango = (planta_config.luz_max - planta_config.luz_min) / 2

        # Temperatura con variación semanal realista
        datos_temperatura = []
        for dia in range(dias):
            variacion = np.sin(dia * 2 * np.pi / 7) * temp_rango * 0.6
            ruido = np.random.normal(0, temp_rango * 0.2)
            valor = temp_promedio + variacion + ruido
            datos_temperatura.append(round(valor, 2))

        # Luz con variación mensual realista
        datos_luz = []
        for dia in range(dias):
            variacion = np.sin(dia * 2 * np.pi / 30) * luz_rango * 0.5
            ruido = np.random.normal(0, luz_rango * 0.15)
            valor = luz_promedio + variacion + ruido
            datos_luz.append(round(valor, 2))

        print(f"OK Tipo: {planta_config.tipo}")
        print(f"OK Humedad optima: {planta_config.humedad_min:.1f}% - {planta_config.humedad_max:.1f}%")
        print(f"OK Temperatura optima: {planta_config.temperatura_min}C - {planta_config.temperatura_max}C")
        print(f"OK Luz optima: {planta_config.luz_min} - {planta_config.luz_max} lux")
        print(f"OK Frecuencia de riego: cada {planta_config.frecuencia_riego_dias} dias")

        # Generar dashboard
        print(f"\nGenerando dashboard...")
        generar_dashboard(
            datos_humedad=datos_humedad,
            datos_temperatura=datos_temperatura,
            datos_luz=datos_luz,
            nombre_planta=f"{planta_config.nombre} ({planta_config.tipo})",
            humedad_optima=(planta_config.humedad_min, planta_config.humedad_max),
            temperatura_optima=(planta_config.temperatura_min, planta_config.temperatura_max),
            luz_optima=(planta_config.luz_min, planta_config.luz_max),
            guardar=guardar,
            nombre_archivo=f"dashboard_{nombre_planta.replace(' ', '_')}.png" if guardar else None
        )

        print(f"\nDashboard generado exitosamente!")

    except Exception as e:
        print(f"\nAdvertencia: No se pudo cargar configuracion de {nombre_planta}")
        print(f"   Error: {e}")
        print(f"\n   Generando dashboard solo con datos de humedad real...")

        # Fallback: generar con valores por defecto
        datos_temperatura = np.random.uniform(18, 26, dias).tolist()
        datos_luz = np.random.uniform(50, 80, dias).tolist()

        generar_dashboard(
            datos_humedad=datos_humedad,
            datos_temperatura=datos_temperatura,
            datos_luz=datos_luz,
            nombre_planta=nombre_planta,
            guardar=guardar
        )


if __name__ == "__main__":
    # Ejemplo de uso: puedes cambiar el nombre de la planta aquí
    plantas_ejemplo = [
        "Aaron's Beard",
        "Acacia",
        "Airplant",
        "Avocado",
        "Aster"
    ]

    print("\nGENERADOR DE DASHBOARD CON DATOS REALES\n")
    print("Plantas de ejemplo disponibles:")
    for i, planta in enumerate(plantas_ejemplo, 1):
        print(f"  {i}. {planta}")

    # Generar dashboard para la primera planta como ejemplo
    print(f"\nGenerando dashboard para: {plantas_ejemplo[0]}")
    generar_dashboard_datos_reales(plantas_ejemplo[0], guardar=False)
