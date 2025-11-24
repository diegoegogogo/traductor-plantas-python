"""
================================================================================
EJEMPLO DE USO DEL DASHBOARD DE PLANTAS
================================================================================

Este archivo muestra diferentes formas de usar el dashboard de visualización.

Ejemplos incluidos:
    1. Dashboard con datos simulados
    2. Dashboard desde archivo CSV
    3. Integración con el traductor de plantas existente
    4. Dashboard con datos personalizados

================================================================================
"""

from dashboard_plantas import (
    generar_dashboard,
    generar_dashboard_desde_csv,
    demo_dashboard
)
import numpy as np


def ejemplo_1_datos_simulados():
    """
    Ejemplo 1: Generar dashboard con datos simulados.
    Útil para probar o cuando no tienes datos reales aún.
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Dashboard con datos simulados")
    print("="*80)

    # Generar 30 días de datos simulados
    dias = 30

    # Humedad: Patrón de riego cada 5 días
    humedad = []
    for dia in range(dias):
        if dia % 5 == 0:
            valor = 70 + np.random.uniform(-3, 3)
        else:
            decaimiento = (dia % 5) * 4
            valor = 70 - decaimiento + np.random.uniform(-2, 2)
        humedad.append(max(30, min(80, valor)))

    # Temperatura: Variación día/noche
    temperatura = [22 + np.sin(d * 0.5) * 3 + np.random.uniform(-1, 1)
                   for d in range(dias)]

    # Luz: Ciclo semanal
    luz = [65 + np.sin(d * 2 * np.pi / 7) * 10 + np.random.uniform(-3, 3)
           for d in range(dias)]

    # Generar dashboard
    generar_dashboard(
        datos_humedad=humedad,
        datos_temperatura=temperatura,
        datos_luz=luz,
        nombre_planta="Rosa del Jardín",
        humedad_optima=(50, 75),
        temperatura_optima=(18, 26),
        luz_optima=(60, 85),
        guardar=False  # Cambiar a True para guardar como imagen
    )

    print("\nDashboard generado y mostrado en ventana emergente")


def ejemplo_2_desde_csv():
    """
    Ejemplo 2: Generar dashboard desde archivo CSV.
    Lee datos directamente del archivo de plantas.
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Dashboard desde archivo CSV")
    print("="*80)

    # Verificar si existe el archivo CSV
    import os
    archivo_csv = "dataset_plantas_960.csv"

    if not os.path.exists(archivo_csv):
        print(f"\nAdvertencia: El archivo {archivo_csv} no existe.")
        print("Genera el CSV primero ejecutando el archivo principal.")
        return

    # Generar dashboard para una planta específica
    generar_dashboard_desde_csv(
        archivo_csv=archivo_csv,
        nombre_planta="Acacia",  # Cambia este nombre por cualquier planta del CSV
        humedad_optima=(56.7, 69.79),
        temperatura_optima=(17.3, 24.8),
        luz_optima=(47.5, 65.8),
        guardar=True,  # Guardará la imagen
        nombre_archivo="dashboard_acacia.png"
    )


def ejemplo_3_datos_personalizados():
    """
    Ejemplo 3: Dashboard con tus propios datos de sensores.
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Dashboard con datos personalizados")
    print("="*80)

    # Datos de ejemplo (reemplaza con tus lecturas reales)
    mis_lecturas_humedad = [
        65.2, 63.8, 61.5, 59.3, 57.1, 68.9, 67.2, 65.5, 63.8, 62.1,
        60.4, 58.7, 57.0, 55.3, 70.1, 68.5, 66.9, 65.3, 63.7, 62.1,
        60.5, 58.9, 57.3, 55.7, 72.3, 70.6, 68.9, 67.2, 65.5, 63.8
    ]

    mis_lecturas_temperatura = [
        22.5, 23.1, 21.8, 20.9, 22.3, 23.7, 24.2, 23.5, 22.8, 21.9,
        22.4, 23.0, 23.8, 24.5, 23.9, 22.6, 21.7, 22.2, 23.4, 24.1,
        23.6, 22.9, 22.1, 21.5, 22.8, 23.5, 24.0, 23.3, 22.5, 21.8
    ]

    mis_lecturas_luz = [
        72.5, 75.3, 68.9, 70.2, 73.8, 76.5, 74.1, 71.8, 69.5, 72.3,
        74.9, 77.2, 75.6, 73.4, 71.1, 68.8, 70.5, 73.2, 75.8, 74.3,
        71.9, 69.6, 67.3, 70.1, 72.8, 75.5, 73.9, 71.6, 69.3, 71.0
    ]

    # Generar dashboard
    generar_dashboard(
        datos_humedad=mis_lecturas_humedad,
        datos_temperatura=mis_lecturas_temperatura,
        datos_luz=mis_lecturas_luz,
        nombre_planta="Mi Planta de Interior",
        humedad_optima=(55, 70),
        temperatura_optima=(20, 25),
        luz_optima=(65, 80),
        guardar=True,
        nombre_archivo="mi_planta_dashboard.png"
    )

    print("\nDashboard guardado como: mi_planta_dashboard.png")


def ejemplo_4_comparar_multiples_plantas():
    """
    Ejemplo 4: Generar dashboards para múltiples plantas y compararlas.
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Comparar múltiples plantas")
    print("="*80)

    plantas = [
        {
            "nombre": "Cactus",
            "humedad": np.random.uniform(25, 35, 30).tolist(),
            "temp": np.random.uniform(22, 28, 30).tolist(),
            "luz": np.random.uniform(70, 90, 30).tolist(),
            "humedad_opt": (20, 40),
            "temp_opt": (20, 30),
            "luz_opt": (65, 95)
        },
        {
            "nombre": "Helecho",
            "humedad": np.random.uniform(65, 80, 30).tolist(),
            "temp": np.random.uniform(18, 24, 30).tolist(),
            "luz": np.random.uniform(40, 60, 30).tolist(),
            "humedad_opt": (60, 85),
            "temp_opt": (16, 26),
            "luz_opt": (35, 65)
        }
    ]

    for planta in plantas:
        print(f"\nGenerando dashboard para: {planta['nombre']}")
        generar_dashboard(
            datos_humedad=planta['humedad'],
            datos_temperatura=planta['temp'],
            datos_luz=planta['luz'],
            nombre_planta=planta['nombre'],
            humedad_optima=planta['humedad_opt'],
            temperatura_optima=planta['temp_opt'],
            luz_optima=planta['luz_opt'],
            guardar=True,
            nombre_archivo=f"dashboard_{planta['nombre'].lower()}.png"
        )

    print("\nDashboards generados para todas las plantas")


def menu_interactivo():
    """
    Menú interactivo para elegir qué ejemplo ejecutar.
    """
    print("\n" + "="*80)
    print("DASHBOARD DE PLANTAS - MENU DE EJEMPLOS")
    print("="*80)
    print("\nSelecciona un ejemplo para ejecutar:")
    print("  1. Dashboard con datos simulados")
    print("  2. Dashboard desde archivo CSV")
    print("  3. Dashboard con datos personalizados")
    print("  4. Comparar múltiples plantas")
    print("  5. Demo rápida")
    print("  0. Salir")

    while True:
        try:
            opcion = input("\nIngresa tu opción (0-5): ").strip()

            if opcion == "1":
                ejemplo_1_datos_simulados()
                break
            elif opcion == "2":
                ejemplo_2_desde_csv()
                break
            elif opcion == "3":
                ejemplo_3_datos_personalizados()
                break
            elif opcion == "4":
                ejemplo_4_comparar_multiples_plantas()
                break
            elif opcion == "5":
                demo_dashboard()
                break
            elif opcion == "0":
                print("\nSaliendo...")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario. Saliendo...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break


# ===== EJECUTAR =====
if __name__ == "__main__":
    # Opción 1: Ejecutar menú interactivo
    menu_interactivo()

    # Opción 2: Ejecutar un ejemplo específico directamente
    # Descomenta la línea que quieras ejecutar:

    # ejemplo_1_datos_simulados()
    # ejemplo_2_desde_csv()
    # ejemplo_3_datos_personalizados()
    # ejemplo_4_comparar_multiples_plantas()
    # demo_dashboard()
