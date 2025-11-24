"""
================================================================================
DASHBOARD DE VISUALIZACIÓN PARA TRADUCTOR DE PLANTAS
================================================================================

Módulo de graficación avanzada para el sistema de monitoreo de plantas.
Genera dashboards interactivos con múltiples gráficos de análisis.

Características:
    - Dashboard con 4 gráficos simultáneos
    - Evolución temporal de humedad (30 días)
    - Comparación con rangos óptimos
    - Distribución de estados de planta
    - Métricas de temperatura y luz

Requisitos:
    - matplotlib
    - numpy
    - pandas (opcional)

Uso:
    from dashboard_plantas import generar_dashboard
    generar_dashboard(datos_planta, nombre_planta="Mi Planta")

================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

# Importar desde el módulo de configuración de plantas
from planta_config import buscar_planta, cargar_plantas

# Configuración de estilo para gráficos
plt.style.use('seaborn-v0_8-darkgrid')
COLORES = {
    'primario': '#2ecc71',
    'secundario': '#3498db',
    'peligro': '#e74c3c',
    'advertencia': '#f39c12',
    'info': '#9b59b6',
    'exito': '#27ae60',
    'neutro': '#95a5a6'
}


def generar_dashboard_con_datos(
    nombre: str,
    dias: int = 30,
    guardar: bool = False,
    nombre_archivo: Optional[str] = None
) -> None:
    """
    Genera un dashboard para una planta específica con datos simulados realistas.

    Busca la planta por nombre y genera datos simulados de humedad, temperatura
    y luz basados en los parámetros óptimos de la planta, con variación realista.

    Args:
        nombre: Nombre de la planta a buscar (ej: "Acacia", "Monstera")
        dias: Número de días de datos a simular (default: 30)
        guardar: Si True, guarda la imagen en lugar de mostrarla
        nombre_archivo: Nombre del archivo a guardar (si guardar=True)

    Ejemplo:
        >>> generar_dashboard_con_datos("Acacia")
        >>> generar_dashboard_con_datos("Monstera", dias=60, guardar=True)
    """
    # Buscar configuración de la planta
    planta = buscar_planta(nombre)

    # Generar datos realistas de humedad con variación y patrón de riego
    humedad_promedio = planta.humedad_promedio
    humedad_desv = planta.humedad_desviacion
    frecuencia_riego = planta.frecuencia_riego_dias

    datos_humedad = []
    for dia in range(dias):
        # Simular patrón de riego: pico cada N días, luego decaimiento
        dias_desde_riego = dia % frecuencia_riego

        if dias_desde_riego == 0:
            # Día de riego: valor cercano al máximo
            valor = np.random.normal(planta.humedad_max - 5, humedad_desv)
        else:
            # Decaimiento gradual hasta el próximo riego
            factor_decaimiento = dias_desde_riego / frecuencia_riego
            valor_base = planta.humedad_max - (planta.humedad_max - planta.humedad_min) * factor_decaimiento
            valor = np.random.normal(valor_base, humedad_desv)

        # Limitar a rango válido
        valor = max(planta.humedad_min - 5, min(planta.humedad_max + 5, valor))
        datos_humedad.append(round(valor, 2))

    # Generar datos realistas de temperatura con variación diaria/semanal
    temp_promedio = (planta.temperatura_min + planta.temperatura_max) / 2
    temp_rango = (planta.temperatura_max - planta.temperatura_min) / 2

    datos_temperatura = []
    for dia in range(dias):
        # Variación sinusoidal semanal + ruido diario
        variacion_semanal = np.sin(dia * 2 * np.pi / 7) * temp_rango * 0.6
        ruido = np.random.normal(0, temp_rango * 0.2)
        valor = temp_promedio + variacion_semanal + ruido

        # Limitar a rango válido
        valor = max(planta.temperatura_min - 2, min(planta.temperatura_max + 2, valor))
        datos_temperatura.append(round(valor, 2))

    # Generar datos realistas de luz con variación estacional
    luz_promedio = (planta.luz_min + planta.luz_max) / 2
    luz_rango = (planta.luz_max - planta.luz_min) / 2

    datos_luz = []
    for dia in range(dias):
        # Variación sinusoidal mensual (estacional) + ruido
        variacion_estacional = np.sin(dia * 2 * np.pi / 30) * luz_rango * 0.5
        ruido = np.random.normal(0, luz_rango * 0.15)
        valor = luz_promedio + variacion_estacional + ruido

        # Limitar a rango válido
        valor = max(planta.luz_min - 5, min(planta.luz_max + 5, valor))
        datos_luz.append(round(valor, 2))

    # Generar dashboard con los datos simulados
    generar_dashboard(
        datos_humedad=datos_humedad,
        datos_temperatura=datos_temperatura,
        datos_luz=datos_luz,
        nombre_planta=f"{planta.nombre} ({planta.tipo})",
        humedad_optima=(planta.humedad_min, planta.humedad_max),
        temperatura_optima=(planta.temperatura_min, planta.temperatura_max),
        luz_optima=(planta.luz_min, planta.luz_max),
        guardar=guardar,
        nombre_archivo=nombre_archivo
    )


def generar_dashboard(
    datos_humedad: List[float],
    datos_temperatura: List[float],
    datos_luz: List[float],
    nombre_planta: str = "Planta",
    humedad_optima: tuple = (40.0, 70.0),
    temperatura_optima: tuple = (18.0, 26.0),
    luz_optima: tuple = (50.0, 80.0),
    guardar: bool = False,
    nombre_archivo: Optional[str] = None,
) -> None:
    """
    Genera un dashboard completo con 4 gráficos de análisis de planta.

    Args:
        datos_humedad: Lista de lecturas de humedad (%) de los últimos 30 días
        datos_temperatura: Lista de lecturas de temperatura (°C)
        datos_luz: Lista de lecturas de luz (%)
        nombre_planta: Nombre de la planta para el título
        humedad_optima: Tupla (min, max) de humedad óptima
        temperatura_optima: Tupla (min, max) de temperatura óptima
        luz_optima: Tupla (min, max) de luz óptima
        guardar: Si True, guarda la imagen en lugar de mostrarla
        nombre_archivo: Nombre del archivo a guardar (si guardar=True)

    Ejemplo:
        >>> humedad = [55.2, 54.8, 53.9, ..., 52.1]  # 30 valores
        >>> temp = [22.5, 23.1, 21.8, ..., 22.9]
        >>> luz = [65.3, 68.2, 70.1, ..., 67.5]
        >>> generar_dashboard(humedad, temp, luz, "Cactus del Desierto")
    """

    # Validar longitud de datos
    dias = len(datos_humedad)
    if len(datos_temperatura) != dias or len(datos_luz) != dias:
        print("⚠️  Advertencia: Las listas de datos tienen longitudes diferentes")
        dias = min(len(datos_humedad), len(datos_temperatura), len(datos_luz))
        datos_humedad = datos_humedad[:dias]
        datos_temperatura = datos_temperatura[:dias]
        datos_luz = datos_luz[:dias]

    # Crear figura con 4 subgráficos (2x2)
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle(f'Dashboard de Monitoreo: {nombre_planta}',
                 fontsize=18, fontweight='bold', y=0.98)

    # ===== GRÁFICO 1: Evolución de Humedad (30 días) =====
    ax1 = plt.subplot(2, 2, 1)
    dias_eje = list(range(1, dias + 1))

    # Línea de humedad real
    ax1.plot(dias_eje, datos_humedad,
             color=COLORES['primario'],
             linewidth=2.5,
             marker='o',
             markersize=4,
             label='Humedad medida')

    # Banda de rango óptimo
    ax1.axhspan(humedad_optima[0], humedad_optima[1],
                alpha=0.2, color=COLORES['exito'],
                label='Rango óptimo')

    # Líneas de referencia
    ax1.axhline(y=humedad_optima[0], color=COLORES['advertencia'],
                linestyle='--', linewidth=1, alpha=0.6)
    ax1.axhline(y=humedad_optima[1], color=COLORES['advertencia'],
                linestyle='--', linewidth=1, alpha=0.6)

    # Promedio
    promedio_humedad = np.mean(datos_humedad)
    ax1.axhline(y=float(promedio_humedad), color=COLORES['info'],
                linestyle=':', linewidth=2, label=f'Promedio: {promedio_humedad:.1f}%')

    ax1.set_xlabel('Días', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Humedad del Suelo (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Evolución de Humedad (30 días)', fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='best', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, dias + 1)

    # ===== GRÁFICO 2: Temperatura y Luz =====
    ax2 = plt.subplot(2, 2, 2)

    # Crear eje secundario para luz
    ax2_luz = ax2.twinx()

    # Temperatura
    linea_temp = ax2.plot(dias_eje, datos_temperatura,
                          color=COLORES['peligro'],
                          linewidth=2.5,
                          marker='s',
                          markersize=4,
                          label='Temperatura')

    # Luz
    linea_luz = ax2_luz.plot(dias_eje, datos_luz,
                             color=COLORES['secundario'],
                             linewidth=2.5,
                             marker='^',
                             markersize=4,
                             label='Luz')

    # Bandas óptimas
    ax2.axhspan(temperatura_optima[0], temperatura_optima[1],
                alpha=0.15, color=COLORES['peligro'])
    ax2_luz.axhspan(luz_optima[0], luz_optima[1],
                    alpha=0.15, color=COLORES['secundario'])

    # Configuración de ejes
    ax2.set_xlabel('Días', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Temperatura (°C)', fontsize=11, fontweight='bold', color=COLORES['peligro'])
    ax2_luz.set_ylabel('Luz (%)', fontsize=11, fontweight='bold', color=COLORES['secundario'])
    ax2.set_title('Temperatura y Niveles de Luz', fontsize=13, fontweight='bold', pad=10)

    # Combinar leyendas
    lineas = linea_temp + linea_luz
    etiquetas = [l.get_label() for l in lineas]
    ax2.legend(handles=lineas, labels=etiquetas, loc='best', framealpha=0.9)

    ax2.tick_params(axis='y', labelcolor=COLORES['peligro'])
    ax2_luz.tick_params(axis='y', labelcolor=COLORES['secundario'])
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, dias + 1)

    # ===== GRÁFICO 3: Distribución de Estados =====
    ax3 = plt.subplot(2, 2, 3)

    # Calcular estados basados en los rangos
    estados = calcular_distribucion_estados(
        datos_humedad, datos_temperatura, datos_luz,
        humedad_optima, temperatura_optima, luz_optima
    )

    # Crear gráfico de barras
    nombres_estados = list(estados.keys())
    valores_estados = list(estados.values())
    colores_barras = [COLORES['exito'], COLORES['advertencia'], COLORES['peligro']]

    barras = ax3.bar(nombres_estados, valores_estados,
                     color=colores_barras,
                     edgecolor='black',
                     linewidth=1.5,
                     alpha=0.8)

    # Añadir valores en las barras
    for i, (barra, valor) in enumerate(zip(barras, valores_estados)):
        height = barra.get_height()
        ax3.text(barra.get_x() + barra.get_width()/2., height,
                f'{valor}\n({valor/dias*100:.0f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax3.set_ylabel('Número de Días', fontsize=11, fontweight='bold')
    ax3.set_title('Distribución de Estados de Salud', fontsize=13, fontweight='bold', pad=10)
    ax3.set_ylim(0, max(valores_estados) * 1.2)
    ax3.grid(True, axis='y', alpha=0.3)

    # ===== GRÁFICO 4: Comparación con Rangos Óptimos =====
    ax4 = plt.subplot(2, 2, 4)

    # Calcular promedios
    promedios_reales = [
        np.mean(datos_humedad),
        np.mean(datos_temperatura),
        np.mean(datos_luz)
    ]

    promedios_optimos = [
        np.mean(humedad_optima),
        np.mean(temperatura_optima),
        np.mean(luz_optima)
    ]

    # Categorías
    categorias = ['Humedad\n(%)', 'Temperatura\n(°C)', 'Luz\n(%)']
    x_pos = np.arange(len(categorias))
    width = 0.35

    # Barras comparativas
    barras1 = ax4.bar(x_pos - width/2, promedios_reales, width,
                      label='Promedio Real',
                      color=COLORES['primario'],
                      edgecolor='black',
                      linewidth=1.5,
                      alpha=0.8)

    barras2 = ax4.bar(x_pos + width/2, promedios_optimos, width,
                      label='Óptimo Ideal',
                      color=COLORES['info'],
                      edgecolor='black',
                      linewidth=1.5,
                      alpha=0.8)

    # Añadir valores en las barras
    for barras in [barras1, barras2]:
        for barra in barras:
            height = barra.get_height()
            ax4.text(barra.get_x() + barra.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax4.set_ylabel('Valor Promedio', fontsize=11, fontweight='bold')
    ax4.set_title('Comparación: Real vs Óptimo', fontsize=13, fontweight='bold', pad=10)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(categorias, fontsize=10)
    ax4.legend(loc='upper right', framealpha=0.9)
    ax4.grid(True, axis='y', alpha=0.3)

    # Ajustar espaciado
    plt.tight_layout(rect=(0, 0.03, 1, 0.96))

    # Añadir timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.text(0.99, 0.01, f'Generado: {timestamp}',
             ha='right', va='bottom', fontsize=8, style='italic', alpha=0.6)

    # Guardar o mostrar
    if guardar:
        if nombre_archivo is None:
            nombre_archivo = f"dashboard_{nombre_planta.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        print(f"Dashboard guardado exitosamente: {nombre_archivo}")
    else:
        plt.show()

    plt.close()


def calcular_distribucion_estados(
    humedad: List[float],
    temperatura: List[float],
    luz: List[float],
    humedad_optima: tuple,
    temperatura_optima: tuple,
    luz_optima: tuple
) -> Dict[str, int]:
    """
    Calcula la distribución de estados de salud de la planta.

    Args:
        humedad: Lista de lecturas de humedad
        temperatura: Lista de lecturas de temperatura
        luz: Lista de lecturas de luz
        humedad_optima: Rango óptimo de humedad
        temperatura_optima: Rango óptimo de temperatura
        luz_optima: Rango óptimo de luz

    Returns:
        Diccionario con conteo de días en cada estado
    """
    estados = {'Óptimo': 0, 'Aceptable': 0, 'Crítico': 0}

    for h, t, l in zip(humedad, temperatura, luz):
        problemas = 0

        # Verificar humedad
        if not (humedad_optima[0] <= h <= humedad_optima[1]):
            problemas += 1

        # Verificar temperatura
        if not (temperatura_optima[0] <= t <= temperatura_optima[1]):
            problemas += 1

        # Verificar luz
        if not (luz_optima[0] <= l <= luz_optima[1]):
            problemas += 1

        # Clasificar estado
        if problemas == 0:
            estados['Óptimo'] += 1
        elif problemas == 1:
            estados['Aceptable'] += 1
        else:
            estados['Crítico'] += 1

    return estados


def generar_dashboard_desde_csv(
    archivo_csv: str,
    nombre_planta: str,
    **kwargs
) -> None:
    """
    Genera dashboard leyendo datos desde un archivo CSV.

    Args:
        archivo_csv: Ruta al archivo CSV con columnas: Día_1, Día_2, etc.
        nombre_planta: Nombre de la planta a graficar
        **kwargs: Argumentos adicionales para generar_dashboard()

    Ejemplo:
        >>> generar_dashboard_desde_csv(
        ...     "plantas_humedad_30dias.csv",
        ...     "Acacia",
        ...     guardar=True
        ... )
    """
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas no esta instalado.")
        print("   Instala con: pip install pandas")
        return

    # Leer CSV
    df = pd.read_csv(archivo_csv)

    # Buscar la planta
    planta_data = df[df['Planta'] == nombre_planta]

    if planta_data.empty:
        print(f"ERROR: Planta '{nombre_planta}' no encontrada en {archivo_csv}")
        print(f"   Plantas disponibles: {', '.join(df['Planta'].head(10).tolist())}...")
        return

    # Extraer datos de humedad (columnas Día_1 a Día_30)
    columnas_dias = [col for col in df.columns if col.startswith('Día_')]
    datos_humedad = planta_data[columnas_dias].values[0].tolist()

    # Generar datos simulados de temperatura y luz (si no están en CSV)
    dias = len(datos_humedad)
    datos_temperatura = np.random.uniform(18, 26, dias).tolist()
    datos_luz = np.random.uniform(50, 80, dias).tolist()

    print(f"Generando dashboard para: {nombre_planta}")
    print(f"   Dias de datos: {dias}")

    # Generar dashboard
    generar_dashboard(
        datos_humedad,
        datos_temperatura,
        datos_luz,
        nombre_planta=nombre_planta,
        **kwargs
    )


def demo_dashboard():
    """
    Función de demostración con datos simulados realistas.
    """
    print("="*80)
    print("Dashboard de Visualización de Plantas")
    print("="*80)

    # Generar datos simulados de 30 días
    dias = 30

    # Humedad: Simular patrón de riego cada 7 días
    humedad_base = 55
    datos_humedad = []
    for dia in range(dias):
        if dia % 7 == 0:  # Día de riego
            humedad = humedad_base + np.random.uniform(10, 15)
        else:
            # Decaimiento gradual
            dias_desde_riego = dia % 7
            humedad = humedad_base - (dias_desde_riego * 3) + np.random.uniform(-2, 2)
        datos_humedad.append(max(30, min(80, humedad)))

    # Temperatura: Variación diaria con patrón semanal
    datos_temperatura = []
    for dia in range(dias):
        temp_base = 22 + np.sin(dia * 2 * np.pi / 7) * 3
        temp = temp_base + np.random.uniform(-1.5, 1.5)
        datos_temperatura.append(temp)

    # Luz: Variación estacional
    datos_luz = []
    for dia in range(dias):
        luz_base = 65 + np.sin(dia * 2 * np.pi / 30) * 10
        luz = luz_base + np.random.uniform(-5, 5)
        datos_luz.append(max(40, min(90, luz)))

    # Generar dashboard
    generar_dashboard(
        datos_humedad=datos_humedad,
        datos_temperatura=datos_temperatura,
        datos_luz=datos_luz,
        nombre_planta="Cactus del Desierto (Demo)",
        humedad_optima=(40, 70),
        temperatura_optima=(18, 26),
        luz_optima=(50, 80),
        guardar=False
    )

    print("\nDemo completada exitosamente!")


# ===== EJECUCIÓN PRINCIPAL =====
if __name__ == "__main__":
    import sys

    print(__doc__)

    # Usar datos reales en lugar de demo
    print("\n" + "="*80)
    print("DASHBOARD CON DATOS REALES DE PLANTAS")
    print("="*80)

    # Verificar si se pasó un nombre de planta como argumento
    if len(sys.argv) > 1:
        nombre_planta = sys.argv[1]
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        guardar = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False
    else:
        # Modo interactivo: preguntar al usuario
        print("\nEjemplos de plantas disponibles:")
        print("  - Acacia, Airplant, Alpine Buttercup")
        print("  - Alumroot, American Globeflower, Angelwing Jasmine")
        print("  - Aaron's Beard, Absaroka Range Beardtongue")
        print("\nTip: Tambien puedes usar: python dashboard_plantas.py NombrePlanta [dias] [guardar]")

        # Preguntar nombre de la planta
        nombre_planta = input("\nIngrese el nombre de la planta que desea visualizar o escriba \"random\": ").strip()

        # Si el usuario escribe "random", seleccionar una planta aleatoria
        if nombre_planta.lower() == "random":
            plantas_disponibles = cargar_plantas()
            if plantas_disponibles:
                planta_aleatoria = random.choice(plantas_disponibles)
                nombre_planta = planta_aleatoria.nombre
                print(f"✨ Planta aleatoria seleccionada: {nombre_planta} ({planta_aleatoria.tipo})")
            else:
                print("Error: No se pudieron cargar las plantas disponibles.")
                nombre_planta = ""

        # Preguntar cantidad de días
        while True:
            try:
                dias_input = input("Ingrese la cantidad de dias de datos a simular (7, 15, 30): ").strip()
                if dias_input == "":
                    dias = 30
                    break
                dias = int(dias_input)
                if dias > 0 and dias <= 365:
                    break
                else:
                    print("Por favor ingrese un valor entre 1 y 365")
            except ValueError:
                print("Por favor ingrese un numero valido")

        # Preguntar si desea guardar
        guardar_input = input("Desea guardar el dashboard como imagen? (s/n, default: n): ").strip().lower()
        guardar = guardar_input in ['s', 'si', 'yes', 'y']

    if nombre_planta:
        try:
            # Generar dashboard con datos reales de la planta
            print(f"\nGenerando dashboard para '{nombre_planta}' con {dias} dias de datos...")
            generar_dashboard_con_datos(nombre_planta, dias=dias, guardar=guardar)
            print("\nOK - Dashboard generado exitosamente!")
        except ValueError as e:
            print(f"\nError: {e}")
            print("\nIntentando con planta de ejemplo (Acacia)...")
            generar_dashboard_con_datos("Acacia", dias=30, guardar=False)
    else:
        print("\nNo se ingreso ningun nombre. Usando planta de ejemplo (Acacia)...")
        generar_dashboard_con_datos("Acacia", dias=30, guardar=False)


from typing import Optional

def set_label(label: Optional[str]) -> None:
    if label is None:
        label = ""  # normalizar a cadena
    # ...usar label seguro como str...
