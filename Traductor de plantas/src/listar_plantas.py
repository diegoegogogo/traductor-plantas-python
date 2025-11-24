"""
Script para listar todas las plantas disponibles en la base de datos.
"""

from planta_config import cargar_plantas

def listar_todas_las_plantas():
    """Lista todas las plantas disponibles con sus características."""
    plantas = cargar_plantas()

    print("="*80)
    print(f"BASE DE DATOS DE PLANTAS - Total: {len(plantas)} plantas")
    print("="*80)
    print()

    # Agrupar por tipo si es necesario
    print(f"{'#':<5} {'Nombre':<40} {'Humedad':<15} {'Temp (C)':<15}")
    print("-"*80)

    for i, planta in enumerate(plantas, 1):
        humedad_rango = f"{planta.humedad_min:.1f}-{planta.humedad_max:.1f}%"
        temp_rango = f"{planta.temperatura_min:.1f}-{planta.temperatura_max:.1f}"

        print(f"{i:<5} {planta.nombre:<40} {humedad_rango:<15} {temp_rango:<15}")

    print("="*80)
    print(f"\nTotal: {len(plantas)} plantas disponibles")
    print("\nPara generar un dashboard, usa:")
    print('  python dashboard_plantas.py "NombrePlanta"')
    print("\nEjemplo:")
    print('  python dashboard_plantas.py "Acacia"')


if __name__ == "__main__":
    listar_todas_las_plantas()
