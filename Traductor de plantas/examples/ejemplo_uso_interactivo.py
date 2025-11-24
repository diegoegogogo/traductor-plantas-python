"""
Script de ejemplo que demuestra el uso del dashboard de forma programática.
Útil para evitar las preguntas interactivas durante pruebas o scripts automatizados.
"""

from dashboard_plantas import generar_dashboard_con_datos

# Ejemplo 1: Dashboard de Acacia con 30 días
print("="*80)
print("Ejemplo 1: Dashboard de Acacia con 30 días")
print("="*80)
generar_dashboard_con_datos("Acacia", dias=30, guardar=False)

# Ejemplo 2: Dashboard de Airplant con 60 días
print("\n" + "="*80)
print("Ejemplo 2: Dashboard de Airplant con 60 días")
print("="*80)
generar_dashboard_con_datos("Airplant", dias=60, guardar=False)

# Ejemplo 3: Dashboard de Alpine Buttercup con 45 días y guardar
print("\n" + "="*80)
print("Ejemplo 3: Dashboard de Alpine Buttercup con 45 días (guardado)")
print("="*80)
generar_dashboard_con_datos("Alpine Buttercup", dias=45, guardar=True)

print("\n✓ Todos los ejemplos completados!")
