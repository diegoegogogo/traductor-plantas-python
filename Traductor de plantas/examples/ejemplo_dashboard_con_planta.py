"""
Ejemplo de uso de generar_dashboard_con_datos()

Este script demuestra cómo generar dashboards para plantas específicas
usando la nueva función que integra el sistema JSON.
"""

from dashboard_plantas import generar_dashboard_con_datos
from planta_config import listar_nombres_plantas

def main():
    print("="*70)
    print("EJEMPLO: GENERAR DASHBOARD PARA PLANTA ESPECÍFICA")
    print("="*70)

    # Ejemplo 1: Dashboard para Acacia
    print("\n[Ejemplo 1] Generando dashboard para Acacia...")
    try:
        generar_dashboard_con_datos("Acacia", dias=30)
        print("✓ Dashboard generado exitosamente")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Ejemplo 2: Dashboard para Alpine Buttercup con más días
    print("\n[Ejemplo 2] Generando dashboard para Alpine Buttercup (60 días)...")
    try:
        generar_dashboard_con_datos("Alpine Buttercup", dias=60)
        print("✓ Dashboard generado exitosamente")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Ejemplo 3: Guardar dashboard en archivo
    print("\n[Ejemplo 3] Guardando dashboard de Aaron's Beard...")
    try:
        generar_dashboard_con_datos(
            "Aaron's Beard",
            dias=30,
            guardar=True,
            nombre_archivo="dashboard_aarons_beard.png"
        )
        print("✓ Dashboard guardado en: dashboard_aarons_beard.png")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Ejemplo 4: Mostrar algunas plantas disponibles
    print("\n[Ejemplo 4] Mostrando primeras 10 plantas disponibles:")
    try:
        nombres = listar_nombres_plantas()
        print(f"\nTotal de plantas disponibles: {len(nombres)}")
        print("\nPrimeras 10:")
        for i, nombre in enumerate(nombres[:10], 1):
            print(f"  {i:2d}. {nombre}")
        print("\nPuedes usar cualquiera de estos nombres con:")
        print("  generar_dashboard_con_datos('Nombre de la planta')")
    except Exception as e:
        print(f"✗ Error: {e}")


def ejemplo_interactivo():
    """
    Ejemplo interactivo que permite al usuario elegir una planta.
    """
    from planta_config import listar_nombres_plantas, buscar_planta

    print("\n" + "="*70)
    print("MODO INTERACTIVO")
    print("="*70)

    nombres = listar_nombres_plantas()
    print(f"\nHay {len(nombres)} plantas disponibles.")

    while True:
        nombre = input("\nIngresa el nombre de una planta (o 'salir' para terminar): ").strip()

        if nombre.lower() == 'salir':
            print("¡Hasta luego!")
            break

        try:
            # Verificar que la planta existe
            planta = buscar_planta(nombre)
            print(f"\n✓ Planta encontrada: {planta.nombre} ({planta.tipo})")
            print(f"  Humedad óptima: {planta.humedad_min:.1f}% - {planta.humedad_max:.1f}%")
            print(f"  Temperatura óptima: {planta.temperatura_min:.1f}°C - {planta.temperatura_max:.1f}°C")
            print(f"  Frecuencia de riego: cada {planta.frecuencia_riego_dias} días")

            # Preguntar si quiere generar dashboard
            generar = input("\n¿Generar dashboard? (s/n): ").strip().lower()
            if generar == 's':
                dias = input("¿Cuántos días de datos? (default: 30): ").strip()
                dias = int(dias) if dias.isdigit() else 30

                guardar = input("¿Guardar en archivo? (s/n): ").strip().lower()

                if guardar == 's':
                    archivo = f"dashboard_{planta.nombre.replace(' ', '_').lower()}.png"
                    generar_dashboard_con_datos(nombre, dias=dias, guardar=True, nombre_archivo=archivo)
                    print(f"✓ Dashboard guardado en: {archivo}")
                else:
                    generar_dashboard_con_datos(nombre, dias=dias)
                    print("✓ Dashboard generado")

        except ValueError as e:
            print(f"✗ {e}")
            print("\nSugerencias (plantas que empiezan con esa letra):")
            sugerencias = [n for n in nombres if n.lower().startswith(nombre.lower()[:1])][:5]
            for s in sugerencias:
                print(f"  - {s}")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactivo":
            ejemplo_interactivo()
        else:
            # Generar dashboard para la planta especificada
            nombre_planta = " ".join(sys.argv[1:])
            print(f"Generando dashboard para: {nombre_planta}")
            generar_dashboard_con_datos(nombre_planta)
    else:
        # Ejecutar ejemplos predefinidos
        main()

        # Preguntar si quiere modo interactivo
        print("\n" + "="*70)
        interactivo = input("\n¿Quieres probar el modo interactivo? (s/n): ").strip().lower()
        if interactivo == 's':
            ejemplo_interactivo()
