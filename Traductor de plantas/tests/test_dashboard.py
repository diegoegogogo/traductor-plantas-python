"""
Script de prueba para el dashboard con datos reales de plantas.
"""

from dashboard_plantas import generar_dashboard_con_datos

# Generar dashboard para la planta Acacia
print("Generando dashboard para Acacia...")
generar_dashboard_con_datos("Acacia", dias=30, guardar=False)
print("Dashboard generado exitosamente!")
