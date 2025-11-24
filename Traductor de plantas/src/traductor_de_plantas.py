"""
================================================================================
TRADUCTOR DE PLANTAS INTELIGENTE
================================================================================

Sistema de monitoreo y diagnóstico de plantas usando sensores y Machine Learning

Descripción:
    Este sistema traduce las necesidades de las plantas a lenguaje humano
    mediante el análisis de sensores de humedad, luz y temperatura. Utiliza
    un modelo de regresión lineal para predecir la necesidad de riego.

Características principales:
    - Base de datos con 30 especies de plantas pre-configuradas
    - Modelo de Machine Learning para predicción de riego
    - Simulación de sensores (compatible con Arduino/ESP32)
    - Análisis inteligente de condiciones ambientales
    - Generación de reportes y estadísticas
    - Exportación de datos a CSV
    - Visualizaciones con matplotlib

Requisitos:
    - Python 3.7+
    - Librerías opcionales: numpy, pandas, matplotlib, scikit-learn
    
Uso:
    python traductor_plantas.py
================================================================================
"""

import random
import time
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional, Any, Union
from enum import Enum

# Importar sistema de configuración de plantas desde JSON
from planta_config import cargar_plantas as _cargar_plantas_json, PlantaConfig

# ==========================================
# IMPORTS OPCIONALES
# ==========================================

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    LIBRERIAS_DISPONIBLES = True
except ImportError:
    LIBRERIAS_DISPONIBLES = False
    print("="*70)
    print("⚠️  MODO BÁSICO ACTIVADO")
    print("="*70)
    print("Librerías avanzadas no disponibles.")
    print("El programa funcionará con capacidades reducidas.")
    print("\nPara habilitar todas las funciones, instala:")
    print("  pip install numpy pandas matplotlib scikit-learn")
    print("="*70 + "\n")


# ==========================================
# ENUMERACIONES Y CONSTANTES
# ==========================================

class EstadoPlanta(Enum):
    """
    Enumeración de estados emocionales posibles de una planta.
    
    Representa el estado general de bienestar de la planta basado en
    el análisis de múltiples parámetros ambientales.
    
    Atributos:
        FELIZ: La planta está en condiciones óptimas (🌿)
        TRISTE: La planta tiene necesidades no críticas (🥀)
        PREOCUPADA: La planta tiene problemas menores (😰)
        ESTRESADA: La planta tiene problemas moderados (😫)
        CRITICA: La planta está en estado crítico (⚠️)
    """
    FELIZ = "Feliz 🌿"
    TRISTE = "Triste 🥀"
    PREOCUPADA = "Preocupada 😰"
    ESTRESADA = "Estresada 😫"
    CRITICA = "Estado Crítico ⚠️"


# ==========================================
# CLASES DE DATOS
# ==========================================

@dataclass
class ConfiguracionPlanta:
    """
    Configuración de parámetros ambientales óptimos para una especie de planta.
    
    Esta clase define los rangos ideales de humedad, temperatura y luz
    para el crecimiento saludable de una planta específica.
    
    Atributos:
        nombre (str): Nombre común de la planta
        humedad_min (float): Humedad mínima del suelo en porcentaje (0-100)
        humedad_max (float): Humedad máxima del suelo en porcentaje (0-100)
        temperatura_min (float): Temperatura mínima ambiente en °C
        temperatura_max (float): Temperatura máxima ambiente en °C
        luz_min (float): Nivel mínimo de luz en porcentaje (0-100)
        luz_max (float): Nivel máximo de luz en porcentaje (0-100)
        umbral_sequia (float): Umbral crítico de humedad (0-1) para activar alertas
        frecuencia_riego_dias (int): Frecuencia recomendada de riego en días
    
    Ejemplo:
        >>> config = ConfiguracionPlanta(
        ...     nombre="Cactus",
        ...     humedad_min=15.0,
        ...     humedad_max=40.0,
        ...     umbral_sequia=0.35
        ... )
    """
    nombre: str = "Planta Genérica"
    humedad_min: float = 30.0
    humedad_max: float = 80.0
    temperatura_min: float = 15.0
    temperatura_max: float = 28.0
    luz_min: float = 20.0
    luz_max: float = 90.0
    umbral_sequia: float = 0.5
    frecuencia_riego_dias: int = 7
    
    def __post_init__(self):
        """
        Validación automática después de la inicialización.
        
        Verifica que los rangos sean válidos y lanza excepciones si no lo son.
        
        Raises:
            ValueError: Si algún rango es inválido
        """
        if self.humedad_min >= self.humedad_max:
            raise ValueError("humedad_min debe ser menor que humedad_max")
        if self.temperatura_min >= self.temperatura_max:
            raise ValueError("temperatura_min debe ser menor que temperatura_max")
        if self.luz_min >= self.luz_max:
            raise ValueError("luz_min debe ser menor que luz_max")
        if not 0 <= self.umbral_sequia <= 1:
            raise ValueError("umbral_sequia debe estar entre 0 y 1")


@dataclass
class LecturaSensores:
    """
    Estructura para almacenar una lectura completa de sensores.
    
    Contiene tanto los valores crudos del sensor (valores ADC) como
    los valores procesados y normalizados.
    
    Atributos:
        humedad_raw (int): Valor crudo del sensor de humedad (0-1023)
        luz_raw (int): Valor crudo del sensor de luz (0-1023)
        temperatura (float): Temperatura en grados Celsius
        humedad_pct (float): Humedad normalizada en porcentaje (0-100)
        luz_pct (float): Luz normalizada en porcentaje (0-100)
        timestamp (float): Marca de tiempo Unix de la lectura
    
    Nota:
        Los valores raw típicamente provienen de sensores analógicos
        de Arduino (0-1023) o ESP32 (0-4095).
    """
    humedad_raw: int
    luz_raw: int
    temperatura: float
    humedad_pct: float = 0.0
    luz_pct: float = 0.0
    timestamp: float = field(default_factory=time.time)


# ==========================================
# BASE DE DATOS DE PLANTAS
# ==========================================

# Función auxiliar para convertir PlantaConfig a ConfiguracionPlanta
def _convertir_planta_config_a_configuracion(pc: PlantaConfig) -> ConfiguracionPlanta:
    """
    Convierte PlantaConfig (del JSON) a ConfiguracionPlanta (clase local).

    Args:
        pc: Objeto PlantaConfig cargado desde JSON

    Returns:
        ConfiguracionPlanta equivalente
    """
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


# Cargar plantas desde JSON usando cache LRU (mucho más rápido)
# NOTA: La lista de 960 plantas ahora se carga desde plantas.json
BASE_DATOS_PLANTAS: List[ConfiguracionPlanta] = [
    _convertir_planta_config_a_configuracion(p) for p in _cargar_plantas_json()
]

# ==========================================
# FUNCIONES DE UTILIDAD PARA BASE DE DATOS
# ==========================================

def obtener_planta_por_nombre(nombre: str) -> Optional[ConfiguracionPlanta]:
    """
    Busca una planta en la base de datos por su nombre.
    
    La búsqueda no es sensible a mayúsculas/minúsculas y elimina
    espacios en blanco al inicio y final.
    
    Args:
        nombre: Nombre de la planta a buscar (ej: "Monstera", "cactus")
        
    Returns:
        ConfiguracionPlanta si se encuentra la planta, None en caso contrario
        
    Ejemplo:
        >>> config = obtener_planta_por_nombre("Monstera")
        >>> if config:
        ...     print(f"Encontrada: {config.nombre}")
        ... else:
        ...     print("Planta no encontrada")
    """
    nombre_normalizado = nombre.lower().strip()
    
    for planta in BASE_DATOS_PLANTAS:
        if planta.nombre.lower() == nombre_normalizado:
            return planta
    
    return None


def listar_plantas_disponibles() -> None:
    """
    Muestra una lista formateada de todas las plantas disponibles.
    
    Imprime una tabla con el índice, nombre y características clave
    de cada planta en la base de datos.
    
    La tabla incluye:
        - Número de índice (1-30)
        - Nombre de la planta
        - Frecuencia de riego recomendada
        - Rango de humedad óptimo
    
    Ejemplo de salida:
        ================================================================
        🌿 PLANTAS DISPONIBLES EN LA BASE DE DATOS
        ================================================================
         1. Cactus                    | Riego cada 14 días | Humedad: 15-40%
         2. Aloe Vera                 | Riego cada 10 días | Humedad: 20-50%
        ...
    """
    print("\n" + "="*70)
    print("🌿 PLANTAS DISPONIBLES EN LA BASE DE DATOS")
    print("="*70)
    
    for i, planta in enumerate(BASE_DATOS_PLANTAS, 1):
        print(f"{i:2d}. {planta.nombre:25s} | "
              f"Riego cada {planta.frecuencia_riego_dias:2d} días | "
              f"Humedad: {planta.humedad_min:.0f}-{planta.humedad_max:.0f}%")
    
    print("="*70)
    print(f"Total: {len(BASE_DATOS_PLANTAS)} plantas en la base de datos\n")


def generar_dataset_csv(ruta_archivo: str = "dataset_plantas_30.csv") -> Optional[Any]:
    """
    Genera un archivo CSV con datos simulados de las 30 plantas.
    
    Para cada planta, genera 50 días de lecturas simuladas de humedad
    basadas en los rangos óptimos de cada especie.
    
    Args:
        ruta_archivo: Ruta donde se guardará el archivo CSV
                     (default: "dataset_plantas_30.csv")
    
    Returns:
        DataFrame de pandas con los datos generados, o None si las
        librerías no están disponibles
    
    Raises:
        ImportError: Si numpy o pandas no están instalados (capturado internamente)
    
    Estructura del CSV generado:
        - planta: Nombre de la planta
        - dia: Día de la lectura (1-50)
        - humedad: Humedad normalizada (0-1)
        - humedad_pct: Humedad en porcentaje (0-100)
        - umbral_sequia: Umbral crítico de la planta
        - frecuencia_riego: Frecuencia recomendada en días
    
    Ejemplo:
        >>> df = generar_dataset_csv("mis_plantas.csv")
        >>> if df is not None:
        ...     print(f"Dataset generado con {len(df)} registros")
    """
    if not LIBRERIAS_DISPONIBLES:
        print("⚠️  Se requieren numpy y pandas para generar el dataset CSV")
        print("   Instala con: pip install numpy pandas")
        return None
    
    import numpy as np
    import pandas as pd
    
    print("📊 Generando dataset de 30 plantas...")
    
    data = []
    dias_por_planta = 50
    
    for planta_config in BASE_DATOS_PLANTAS:
        # Normalizar rangos de humedad a escala 0-1
        humedad_min_norm = planta_config.humedad_min / 100.0
        humedad_max_norm = planta_config.humedad_max / 100.0
        
        # Generar valores aleatorios dentro del rango óptimo
        humedad_valores = np.random.uniform(
            humedad_min_norm, 
            humedad_max_norm, 
            dias_por_planta
        )
        
        # Crear registros para cada día
        for dia, humedad in enumerate(humedad_valores, 1):
            data.append({
                'planta': planta_config.nombre,
                'dia': dia,
                'humedad': round(humedad, 3),
                'humedad_pct': round(humedad * 100, 2),
                'umbral_sequia': planta_config.umbral_sequia,
                'frecuencia_riego': planta_config.frecuencia_riego_dias
            })
    
    # Crear DataFrame y guardar
    df = pd.DataFrame(data)
    df.to_csv(ruta_archivo, index=False)
    
    print(f"✅ Dataset generado exitosamente: {ruta_archivo}")
    print(f"   📋 Estadísticas:")
    print(f"      • Total de registros: {len(df):,}")
    print(f"      • Plantas incluidas: {len(BASE_DATOS_PLANTAS)}")
    print(f"      • Días por planta: {dias_por_planta}")
    print(f"      • Tamaño del archivo: ~{len(df) * 50 / 1024:.1f} KB")
    
    return df


# ==========================================
# MÓDULO 1: MODELO DE MACHINE LEARNING
# ==========================================

class ModeloPrediccionRiego:
    """
    Modelo de regresión lineal para predecir la necesidad de riego.
    
    Este modelo utiliza regresión lineal simple para predecir si una planta
    necesita agua basándose en el nivel de humedad del suelo. La predicción
    retorna un valor entre 0 y 1, donde:
        - 0 = No necesita agua (humedad óptima)
        - 1 = Necesita agua urgentemente (sequía crítica)
    
    El modelo puede funcionar en dos modos:
        1. Con scikit-learn (si está disponible) - Más preciso
        2. Con implementación matemática pura - Sin dependencias
    
    Atributos:
        entrenado (bool): Indica si el modelo ha sido entrenado
        pendiente (float): Coeficiente m de la ecuación y = mx + b
        intercepto (float): Coeficiente b de la ecuación y = mx + b
        r2_score (float): Coeficiente de determinación R² (calidad del ajuste)
        modelo (LinearRegression): Instancia del modelo sklearn (si disponible)
        usar_sklearn (bool): Indica si se usa sklearn o implementación pura
    
    Ejemplo:
        >>> modelo = ModeloPrediccionRiego()
        >>> modelo.entrenar()  # Entrena con datos por defecto
        >>> necesidad = modelo.predecir(35.0)  # 35% de humedad
        >>> print(f"Necesidad de agua: {necesidad:.2%}")
    """
    
    def __init__(self):
        """
        Inicializa el modelo de predicción.
        
        Detecta automáticamente si scikit-learn está disponible y
        configura el modo de operación correspondiente.
        """
        self.entrenado: bool = False
        self.pendiente: Optional[float] = None
        self.intercepto: Optional[float] = None
        self.r2_score: Optional[float] = None
        self.modelo: Optional[Any] = None
        self.usar_sklearn: bool = False
        
        if LIBRERIAS_DISPONIBLES:
            self.modelo = LinearRegression()
            self.usar_sklearn = True
    
    def entrenar(self, 
                 humedad_datos: Optional[List[float]] = None, 
                 estado_datos: Optional[List[float]] = None) -> 'ModeloPrediccionRiego':
        """
        Entrena el modelo con datos de humedad y necesidad de agua.
        
        Utiliza el método de mínimos cuadrados para encontrar la mejor
        línea de ajuste entre la humedad del suelo y la necesidad de riego.
        
        Args:
            humedad_datos: Lista de valores de humedad (0-100%). 
                          Si es None, usa valores por defecto.
            estado_datos: Lista de valores de necesidad de agua (0-1).
                         1 = necesita agua, 0 = no necesita.
                         Si es None, usa valores por defecto.
        
        Returns:
            self: Retorna la instancia para permitir encadenamiento de métodos
        
        Raises:
            ValueError: Si las listas tienen longitudes diferentes
        
        Nota:
            Los datos por defecto están basados en observaciones empíricas
            de plantas comunes y cubren el rango completo de 0-100% de humedad.
        
        Ejemplo:
            >>> modelo = ModeloPrediccionRiego()
            >>> # Datos personalizados
            >>> humedad = [10, 20, 30, 40, 50, 60, 70, 80]
            >>> necesidad = [1.0, 0.9, 0.7, 0.5, 0.3, 0.1, 0.0, 0.0]
            >>> modelo.entrenar(humedad, necesidad)
        """
        # Datos por defecto: 18 puntos que cubren el rango completo
        if humedad_datos is None:
            humedad_datos = [10, 15, 20, 25, 30, 35, 40, 45, 50, 
                           55, 60, 65, 70, 75, 80, 85, 90, 95]
        
        if estado_datos is None:
            # Curva de necesidad decreciente con la humedad
            estado_datos = [1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7, 0.5, 0.3,
                          0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        # Validación de entrada
        if len(humedad_datos) != len(estado_datos):
            raise ValueError("humedad_datos y estado_datos deben tener la misma longitud")
        
        if self.usar_sklearn and self.modelo is not None:
            # Modo 1: Usar scikit-learn
            import numpy as np
            
            h_array = np.array(humedad_datos).reshape(-1, 1)
            e_array = np.array(estado_datos)
            
            # Entrenar modelo
            self.modelo.fit(h_array, e_array)
            
            # Extraer parámetros
            self.pendiente = self.modelo.coef_[0]
            self.intercepto = self.modelo.intercept_
            
            # Calcular métricas de calidad
            predicciones = self.modelo.predict(h_array)
            self.r2_score = r2_score(e_array, predicciones)
        
        else:
            # Modo 2: Implementación matemática pura
            # Usar el método de mínimos cuadrados ordinarios (OLS)
            
            n = len(humedad_datos)
            
            # Calcular medias
            media_x = sum(humedad_datos) / n
            media_y = sum(estado_datos) / n
            
            # Calcular pendiente usando la fórmula de mínimos cuadrados
            # m = Σ[(xi - x̄)(yi - ȳ)] / Σ[(xi - x̄)²]
            numerador = sum((humedad_datos[i] - media_x) * (estado_datos[i] - media_y) 
                           for i in range(n))
            denominador = sum((humedad_datos[i] - media_x) ** 2 for i in range(n))
            
            self.pendiente = numerador / denominador if denominador != 0 else 0
            
            # Calcular intercepto: b = ȳ - m*x̄
            self.intercepto = media_y - (self.pendiente * media_x)
            
            # Calcular R² manualmente
            # R² = 1 - (SS_res / SS_tot)
            # SS_res = Σ(yi - ŷi)²  (suma de residuos cuadrados)
            # SS_tot = Σ(yi - ȳ)²  (suma total de cuadrados)
            predicciones = [self.pendiente * x + self.intercepto for x in humedad_datos]
            ss_res = sum((estado_datos[i] - predicciones[i]) ** 2 for i in range(n))
            ss_tot = sum((estado_datos[i] - media_y) ** 2 for i in range(n))
            self.r2_score = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        self.entrenado = True
        return self
    
    def predecir(self, humedad: float) -> float:
        """
        Predice la necesidad de agua basándose en el nivel de humedad.
        
        Aplica la ecuación de regresión lineal y = mx + b para calcular
        la necesidad de agua, limitando el resultado entre 0 y 1.
        
        Args:
            humedad: Nivel de humedad del suelo en porcentaje (0-100)
        
        Returns:
            float: Necesidad de agua entre 0 y 1
                  0.0 = No necesita agua
                  0.5 = Umbral de decisión
                  1.0 = Necesita agua urgentemente
        
        Raises:
            ValueError: Si el modelo no ha sido entrenado
        
        Ejemplo:
            >>> modelo = ModeloPrediccionRiego()
            >>> modelo.entrenar()
            >>> necesidad = modelo.predecir(35.0)
            >>> if necesidad > 0.5:
            ...     print("¡Regar la planta!")
            ... else:
            ...     print("La planta está bien")
        """
        if not self.entrenado:
            raise ValueError("El modelo debe ser entrenado antes de hacer predicciones")
        
        if self.usar_sklearn and self.modelo is not None:
            # Usar sklearn
            import numpy as np
            entrada = np.array([[float(humedad)]])
            prediccion = self.modelo.predict(entrada)[0]
        else:
            # Usar implementación pura: y = mx + b
            prediccion = (self.pendiente * humedad) + self.intercepto  # type: ignore
        
        # Limitar resultado entre 0 y 1
        return float(max(0.0, min(1.0, prediccion)))
    
    def obtener_ecuacion(self) -> str:
        """
        Retorna la ecuación del modelo en formato legible.
        
        Returns:
            str: Ecuación en formato "y = mx + b" con valores numéricos
        
        Ejemplo:
            >>> modelo.obtener_ecuacion()
            'y = -0.0175x + 1.2281'
        """
        if self.pendiente is None or self.intercepto is None:
            return "Modelo no entrenado"
        return f"y = {self.pendiente:.4f}x + {self.intercepto:.4f}"
    
    def mostrar_metricas(self) -> None:
        """
        Imprime un resumen detallado de las métricas del modelo.
        
        Muestra:
            - Ecuación del modelo
            - Coeficiente R² (calidad del ajuste)
            - Pendiente e intercepto
            - Método de implementación (scikit-learn o puro)
        
        Interpretación del R²:
            - R² > 0.9: Excelente ajuste
            - 0.7 < R² < 0.9: Buen ajuste
            - 0.5 < R² < 0.7: Ajuste moderado
            - R² < 0.5: Ajuste pobre
        """
        print("\n" + "="*50)
        print("MODELO MATEMÁTICO DE PREDICCIÓN DE RIEGO")
        print("="*50)

        def fmt(val: float | None, fmt_str: str = "{:.4f}") -> str:
            return fmt_str.format(val) if val is not None else "N/A"

        r2 = self.r2_score
        if r2 is None:
            r2_display = "N/A"
            calidad = "Sin evaluar"
        else:
            r2_display = f"{r2:.4f}"
            calidad = ("Excelente" if r2 > 0.9 else
                       "Bueno" if r2 > 0.7 else
                       "Moderado" if r2 > 0.5 else
                       "Pobre")

        print(f"Ecuación: {self.obtener_ecuacion()}")
        print(f"R² Score: {r2_display} ({calidad})")
        print(f"Pendiente (m): {fmt(self.pendiente)}")
        print(f"Intercepto (b): {fmt(self.intercepto)}")
        print(f"Método: {'scikit-learn' if self.usar_sklearn else 'Matemáticas puras (numpy-free)'}")
        print("="*50 + "\n")
    
    def graficar_modelo(self, guardar: bool = False) -> None:
        """
        Genera una visualización gráfica del modelo entrenado.
        
        Crea un gráfico que muestra:
            - Línea de predicción del modelo
            - Umbral de decisión (y=0.5)
            - Zonas de riesgo (necesita agua vs está bien)
            - Ecuación del modelo
        
        Args:
            guardar: Si True, guarda la gráfica como PNG
                    (default: False, solo muestra)
        
        Requires:
            matplotlib debe estar instalado
        
        Ejemplo:
            >>> modelo.graficar_modelo(guardar=True)
            # Genera 'modelo_prediccion_riego.png'
        """
        if not LIBRERIAS_DISPONIBLES:
            print("⚠️  matplotlib no está disponible para graficar")
            print("   Instala con: pip install matplotlib numpy")
            return
        
        import numpy as np
        import matplotlib.pyplot as plt
        
        # Generar datos para la gráfica
        humedad_plot = np.linspace(0, 100, 100)
        
        if self.usar_sklearn and self.modelo is not None:
            predicciones = self.modelo.predict(humedad_plot.reshape(-1, 1))
        else:
            if self.pendiente is not None and self.intercepto is not None:
                predicciones = np.array([float(self.pendiente * h + self.intercepto) 
                                        for h in humedad_plot])
            else:
                print("⚠️  Modelo no entrenado correctamente")
                return
        
        # Crear figura
        plt.figure(figsize=(12, 7))
        
        # Línea de predicción
        plt.plot(humedad_plot, predicciones, 'b-', linewidth=3, 
                label='Modelo de Predicción', zorder=3)
        
        # Umbral de decisión
        plt.axhline(y=0.5, color='orange', linestyle='--', linewidth=2,
                   label='Umbral de Decisión (50%)', zorder=2)
        
        # Zonas de riesgo con conversión explícita a arrays
        pred_array = np.asarray(predicciones, dtype=float)
        humedad_array = np.asarray(humedad_plot, dtype=float)
        
        # Zona crítica (necesita agua)
        where_seq = (pred_array >= 0.5).tolist()   # converts to List[bool]
        plt.fill_between(humedad_array, 0, pred_array,
                 where=where_seq, alpha=0.3,
                 color='red', label='Zona Crítica: Necesita Agua', zorder=1)

        # Zona segura (buena hidratación)
        plt.fill_between(humedad_array, 0, pred_array,
                 where=(pred_array < 0.5).tolist(), alpha=0.3,   # <-- changed
                 color='green', label='Zona Segura: Buena Hidratación', zorder=1)
        
        # Etiquetas y título
        plt.title(f'Modelo de Predicción de Riego\n{self.obtener_ecuacion()} | R² = {self.r2_score:.4f}', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Humedad del Suelo (%)', fontsize=14, fontweight='bold')
        plt.ylabel('Necesidad de Agua (0=Bien, 1=Crítico)', fontsize=14, fontweight='bold')
        
        # Configuración visual
        plt.grid(True, alpha=0.3, linestyle=':', linewidth=1)
        plt.legend(loc='best', fontsize=11, framealpha=0.9)
        plt.ylim(-0.1, 1.1)
        plt.xlim(0, 100)
        
        # Anotaciones
        plt.text(25, 0.9, '⚠️ CRÍTICO', fontsize=12, color='darkred', fontweight='bold')
        plt.text(75, 0.1, '✅ ÓPTIMO', fontsize=12, color='darkgreen', fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar si se solicita
        if guardar:
            nombre_archivo = 'modelo_prediccion_riego.png'
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfica guardada: {nombre_archivo}")
        
        plt.show()


# ==========================================
# MÓDULO 2: TRADUCTOR DE PLANTAS
# ==========================================

class TraductorPlantaInteligente:
    """
    Sistema inteligente de monitoreo y traducción del estado de plantas.
    
    Esta clase integra sensores, procesamiento matemático y machine learning
    para diagnosticar el estado de una planta y traducirlo a lenguaje humano.
    
    Flujo de trabajo:
        1. Lee sensores (reales o simulados)
        2. Normaliza los valores crudos a porcentajes
        3. Analiza las condiciones con el modelo ML
        4. Diagnostica problemas y prioridades
        5. Traduce a lenguaje natural
        6. Almacena en historial para estadísticas
    
    Atributos:
        nombre (str): Nombre personalizado de la planta
        tipo_planta (str): Tipo o especie de la planta
        config (ConfiguracionPlanta): Configuración de parámetros óptimos
        historial (List[LecturaSensores]): Registro de todas las lecturas
        modelo_ml (ModeloPrediccionRiego): Modelo de predicción de riego
    
    Ejemplo de uso completo:
        >>> config = ConfiguracionPlanta(
        ...     nombre="Mi Monstera",
        ...     humedad_min=40.0,
        ...     humedad_max=70.0
        ... )
        >>> traductor = TraductorPlantaInteligente(
        ...     nombre="Monstera Deliciosa",
        ...     tipo_planta="Monstera",
        ...     config=config
        ... )
        >>> lectura, mensaje = traductor.procesar_lectura()
        >>> print(mensaje)
    """
    
    def __init__(self, 
                 nombre: str, 
                 tipo_planta: str = "general",
                 config: Optional[ConfiguracionPlanta] = None):
        """
        Inicializa el sistema de traducción para una planta específica.
        
        Args:
            nombre: Nombre personalizado de la planta individual
            tipo_planta: Tipo o especie (ej: "Monstera", "Cactus")
            config: Configuración de parámetros. Si es None, usa valores genéricos
        """
        self.nombre = nombre
        self.tipo_planta = tipo_planta
        self.config = config if config else ConfiguracionPlanta()
        self.historial: List[LecturaSensores] = []
        self.modelo_ml = ModeloPrediccionRiego()
        
        # Entrenar modelo automáticamente
        self.modelo_ml.entrenar()
    
    def leer_sensores_simulados(self) -> Tuple[int, int, float]:
        """
        Simula la lectura de sensores físicos tipo Arduino/ESP32.
        
        Genera valores aleatorios que imitan sensores reales:
            - Sensores analógicos de humedad y luz: 0-1023 (10 bits)
            - Sensor de temperatura: valores flotantes en °C
        
        En un sistema real, esta función sería reemplazada por:
            - analogRead() para Arduino
            - ADC.read() para ESP32/MicroPython
            - Lectura de GPIO para Raspberry Pi
        
        Returns:
            Tuple[int, int, float]: (humedad_raw, luz_raw, temperatura)
                humedad_raw: Valor ADC 0-1023
                luz_raw: Valor ADC 0-1023
                temperatura: Temperatura en °C
        
        Nota:
            La temperatura incluye ruido gaussiano para simular
            variabilidad realista del sensor.
        
        Ejemplo para integración con hardware real:
            ```python
            def leer_sensores_reales(self):
                import board
                import analogio
                
                # Configurar pines analógicos
                humedad_pin = analogio.AnalogIn(board.A0)
                luz_pin = analogio.AnalogIn(board.A1)
                
                # Leer valores (0-65535 en CircuitPython, escalar a 0-1023)
                humedad_raw = int(humedad_pin.value / 64)
                luz_raw = int(luz_pin.value / 64)
                
                # Leer temperatura de sensor DHT22
                temperatura = dht_sensor.temperature
                
                return humedad_raw, luz_raw, temperatura
            ```
        """
        # Simular valores ADC de 10 bits (0-1023)
        humedad_raw = random.randint(0, 1023)
        luz_raw = random.randint(0, 1023)
        
        # Simular temperatura con distribución realista
        temp_base = random.uniform(18.0, 30.0)
        temp_ruido = random.gauss(0, 0.5)  # Ruido gaussiano ±0.5°C
        temperatura = round(temp_base + temp_ruido, 2)
        
        return humedad_raw, luz_raw, temperatura
    
    @staticmethod
    def normalizar_sensor(valor_crudo: int, rango_max: int = 1023) -> float:
        """
        Normaliza valores crudos de sensores a porcentaje (0-100).
        
        Aplica una transformación lineal para convertir valores ADC
        a un porcentaje más intuitivo para el usuario.
        
        Fórmula matemática:
            f(x) = (x / x_max) × 100
        
        Args:
            valor_crudo: Valor leído del sensor ADC
            rango_max: Valor máximo del ADC (default: 1023 para Arduino)
                      Valores comunes:
                      - Arduino: 1023 (10 bits)
                      - ESP32: 4095 (12 bits)
                      - Raspberry Pi con MCP3008: 1023 (10 bits)
        
        Returns:
            float: Porcentaje normalizado entre 0.0 y 100.0
        
        Raises:
            ValueError: Si rango_max es menor o igual a 0
        
        Ejemplo:
            >>> TraductorPlantaInteligente.normalizar_sensor(512, 1023)
            50.05
            >>> TraductorPlantaInteligente.normalizar_sensor(0, 1023)
            0.0
            >>> TraductorPlantaInteligente.normalizar_sensor(1023, 1023)
            100.0
        """
        if rango_max <= 0:
            raise ValueError("rango_max debe ser mayor que 0")
        
        # Calcular porcentaje
        porcentaje = (valor_crudo / rango_max) * 100
        
        # Asegurar que esté en el rango válido y redondear
        return round(max(0.0, min(100.0, porcentaje)), 2)
    
    def analizar_condiciones(self, lectura: LecturaSensores) -> Dict[str, Any]:
        """
        Analiza las condiciones ambientales y genera un diagnóstico completo.
        
        Realiza un análisis multi-criterio que incluye:
            1. Predicción ML de necesidad de riego
            2. Análisis de rangos de temperatura
            3. Análisis de niveles de luz
            4. Asignación de prioridades a los problemas
            5. Determinación del estado emocional general
        
        Sistema de prioridades:
            - Prioridad 3: Crítico (requiere acción inmediata)
            - Prioridad 2: Alto (requiere atención pronto)
            - Prioridad 1: Bajo (monitoreo)
        
        Args:
            lectura: Objeto LecturaSensores con datos procesados
        
        Returns:
            Dict con las siguientes claves:
                - estado (EstadoPlanta): Estado emocional general
                - problemas (List[str]): Lista de mensajes de problemas
                - prioridad_maxima (int): Mayor prioridad encontrada (0-3)
                - necesidad_agua_ml (float): Predicción del modelo (0-1)
                - lectura (LecturaSensores): Lectura analizada
        
        Lógica de decisión:
            ```
            Humedad ML > 0.7  → Sed extrema (Prioridad 3)
            Humedad ML > 0.5  → Sed moderada (Prioridad 2)
            Humedad > max     → Exceso de agua (Prioridad 2)
            Temp > max + 5°C  → Calor extremo (Prioridad 3)
            Temp > max        → Calor moderado (Prioridad 2)
            Temp < min        → Frío (Prioridad 2)
            Luz < min         → Oscuridad (Prioridad 1)
            Luz > max         → Exceso de luz (Prioridad 2)
            ```
        """
        problemas: List[str] = []
        prioridades: List[int] = []
        
        # ========== ANÁLISIS 1: HUMEDAD CON ML ==========
        necesidad_agua = self.modelo_ml.predecir(lectura.humedad_pct)
        
        if necesidad_agua > 0.7:
            # Sequía crítica
            problemas.append(
                f"💧 URGENTE: Sed extrema (Humedad: {lectura.humedad_pct}%)"
            )
            prioridades.append(3)
        elif necesidad_agua > 0.5:
            # Sequía moderada
            problemas.append(
                f"💧 Tengo sed (Humedad: {lectura.humedad_pct}%)"
            )
            prioridades.append(2)
        elif lectura.humedad_pct > self.config.humedad_max:
            # Exceso de agua
            problemas.append(
                f"🌊 Demasiada agua, riesgo de pudrición "
                f"(Humedad: {lectura.humedad_pct}%)"
            )
            prioridades.append(2)
        
        # ========== ANÁLISIS 2: TEMPERATURA ==========
        if lectura.temperatura > self.config.temperatura_max:
            diferencia = lectura.temperatura - self.config.temperatura_max
            
            if diferencia > 5:
                # Calor extremo
                problemas.append(
                    f"🔥 CRÍTICO: Calor extremo ({lectura.temperatura}°C)"
                )
                prioridades.append(3)
            else:
                # Calor moderado
                problemas.append(
                    f"🔥 Hace mucho calor ({lectura.temperatura}°C)"
                )
                prioridades.append(2)
        
        elif lectura.temperatura < self.config.temperatura_min:
            # Frío
            problemas.append(
                f"❄️ Hace frío ({lectura.temperatura}°C)"
            )
            prioridades.append(2)
        
        # ========== ANÁLISIS 3: LUZ ==========
        if lectura.luz_pct < self.config.luz_min:
            # Poca luz
            problemas.append(
                f"🌑 Muy oscuro, necesito luz (Luz: {lectura.luz_pct}%)"
            )
            prioridades.append(1)
        
        elif lectura.luz_pct > self.config.luz_max:
            # Exceso de luz
            problemas.append(
                f"☀️ Luz muy intensa, me quemo (Luz: {lectura.luz_pct}%)"
            )
            prioridades.append(2)
        
        # ========== DETERMINACIÓN DEL ESTADO GENERAL ==========
        if not problemas:
            estado = EstadoPlanta.FELIZ
        elif max(prioridades, default=0) >= 3:
            estado = EstadoPlanta.CRITICA
        elif max(prioridades, default=0) >= 2:
            estado = EstadoPlanta.ESTRESADA
        else:
            estado = EstadoPlanta.PREOCUPADA
        
        return {
            'estado': estado,
            'problemas': problemas,
            'prioridad_maxima': max(prioridades, default=0),
            'necesidad_agua_ml': necesidad_agua,
            'lectura': lectura
        }
    
    def traducir_mensaje(self, diagnostico: Dict[str, Any]) -> str:
        """
        Convierte el diagnóstico técnico a lenguaje natural humanizado.
        
        Genera un mensaje desde la perspectiva de la planta, usando
        un tono empático y directo que facilita la comprensión del usuario.
        
        Args:
            diagnostico: Diccionario retornado por analizar_condiciones()
        
        Returns:
            str: Mensaje humanizado que la planta "diría"
        
        Formato del mensaje:
            [EMOJI_ESTADO] [NOMBRE] dice: [DESCRIPCIÓN_PROBLEMAS]
        
        Ejemplos de salida:
            - Sin problemas:
              "🌿 Monstera dice: ¡Estoy perfecta! Todo está ideal."
            
            - Un problema:
              "😫 Monstera dice: 💧 Tengo sed (Humedad: 35%)."
            
            - Múltiples problemas:
              "⚠️ Monstera dice: 💧 URGENTE: Sed extrema, 
               🔥 Hace mucho calor y 🌑 Muy oscuro."
        """
        estado: EstadoPlanta = diagnostico['estado']
        problemas: List[str] = diagnostico['problemas']
        
        # Caso feliz: sin problemas
        if not problemas:
            return f"🌿 {self.nombre} dice: ¡Estoy perfecta! Todo está ideal."
        
        # Construir mensaje concatenando problemas
        if len(problemas) == 1:
            # Un solo problema
            mensaje_problemas = problemas[0]
        elif len(problemas) == 2:
            # Dos problemas
            mensaje_problemas = f"{problemas[0]} y {problemas[1]}"
        else:
            # Tres o más problemas
            mensaje_problemas = ", ".join(problemas[:-1]) + f" y {problemas[-1]}"
        
        return f"{estado.value} {self.nombre} dice: {mensaje_problemas}."
    
    def procesar_lectura(self) -> Tuple[LecturaSensores, str]:
        """
        Pipeline completo de procesamiento de una lectura de sensores.
        
        Este es el método principal que ejecuta todo el flujo de trabajo:
        
        Pasos:
            1. Lee sensores (simulados o reales)
            2. Normaliza valores crudos a porcentajes
            3. Crea objeto LecturaSensores con timestamp
            4. Analiza condiciones con ML y reglas
            5. Traduce diagnóstico a lenguaje natural
            6. Guarda en historial para estadísticas
        
        Returns:
            Tuple[LecturaSensores, str]:
                - LecturaSensores: Objeto con todos los datos de la lectura
                - str: Mensaje humanizado del estado de la planta
        
        Ejemplo de uso:
            >>> traductor = TraductorPlantaInteligente("Mi Planta")
            >>> lectura, mensaje = traductor.procesar_lectura()
            >>> print(f"Humedad: {lectura.humedad_pct}%")
            >>> print(mensaje)
            Humedad: 45.3%
            🌿 Mi Planta dice: ¡Estoy perfecta! Todo está ideal.
        """
        # Paso 1: Leer sensores
        h_raw, l_raw, temp = self.leer_sensores_simulados()
        
        # Paso 2: Normalizar datos (ADC → Porcentaje)
        h_pct = self.normalizar_sensor(h_raw)
        l_pct = self.normalizar_sensor(l_raw)
        
        # Paso 3: Crear registro de lectura
        lectura = LecturaSensores(
            humedad_raw=h_raw,
            luz_raw=l_raw,
            temperatura=temp,
            humedad_pct=h_pct,
            luz_pct=l_pct,
            timestamp=time.time()
        )
        
        # Paso 4: Analizar condiciones
        diagnostico = self.analizar_condiciones(lectura)
        
        # Paso 5: Traducir a mensaje
        mensaje = self.traducir_mensaje(diagnostico)
        
        # Paso 6: Guardar en historial
        self.historial.append(lectura)
        
        return lectura, mensaje
    
    def generar_reporte_estadistico(self) -> None:
        """
        Muestra un resumen estadístico completo del historial de lecturas.
        
        Calcula y presenta:
            - Total de lecturas realizadas
            - Estadísticas de humedad (promedio, mín, máx)
            - Estadísticas de temperatura (promedio, mín, máx)
            - Estadísticas de luz (promedio, mín, máx)
        
        El resumen ayuda a identificar patrones y tendencias en las
        condiciones ambientales a lo largo del tiempo.
        
        Nota:
            Requiere al menos una lectura en el historial.
        
        Ejemplo de salida:
            ============================================================
            ESTADÍSTICAS DE MONSTERA DELICIOSA
            ============================================================
            Total de lecturas: 5
            
            Humedad del Suelo:
              • Promedio: 52.34%
              • Mínimo: 45.20%
              • Máximo: 58.90%
            
            Temperatura:
              • Promedio: 23.45°C
              • Mínimo: 21.80°C
              • Máximo: 25.30°C
            
            Luz:
              • Promedio: 67.23%
              • Mínimo: 55.40%
              • Máximo: 78.90%
            ============================================================
        """
        if not self.historial:
            print("\n⚠️  No hay datos históricos disponibles.")
            print("   Realiza algunas lecturas primero.\n")
            return
        
        # Extraer datos del historial
        humedades = [l.humedad_pct for l in self.historial]
        temperaturas = [l.temperatura for l in self.historial]
        luces = [l.luz_pct for l in self.historial]
        
        # Función auxiliar para calcular promedio
        def calcular_promedio(datos: List[float]) -> float:
            """Calcula el promedio de una lista de números."""
            return sum(datos) / len(datos) if datos else 0.0
        
        # Imprimir reporte
        print("\n" + "="*60)
        print(f"ESTADÍSTICAS DE {self.nombre.upper()}")
        print("="*60)
        print(f"Total de lecturas: {len(self.historial)}")
        
        print(f"\nHumedad del Suelo:")
        print(f"  • Promedio: {calcular_promedio(humedades):.2f}%")
        print(f"  • Mínimo: {min(humedades):.2f}%")
        print(f"  • Máximo: {max(humedades):.2f}%")
        
        print(f"\nTemperatura:")
        print(f"  • Promedio: {calcular_promedio(temperaturas):.2f}°C")
        print(f"  • Mínimo: {min(temperaturas):.2f}°C")
        print(f"  • Máximo: {max(temperaturas):.2f}°C")
        
        print(f"\nLuz:")
        print(f"  • Promedio: {calcular_promedio(luces):.2f}%")
        print(f"  • Mínimo: {min(luces):.2f}%")
        print(f"  • Máximo: {max(luces):.2f}%")
        
        print("="*60 + "\n")


# ==========================================
# SCRIPT PRINCIPAL (EJECUCIÓN DIRECTA)
# ==========================================

if __name__ == "__main__":
    """
    Ejecución principal del script.
    
    Este bloque se ejecuta solo si el archivo es corrido como script
    principal (no si es importado como módulo).
    
    Funcionalidad:
        - Mensaje de bienvenida
        - Listar plantas disponibles
        - Opción de generar dataset CSV
        - Ejemplo de uso de TraductorPlantaInteligente
        
    Notas:
        - Asegúrese de tener las librerías necesarias instaladas
        - Para salir del programa, use Ctrl+C en cualquier momento
    """
    print("="*70)
    print("🌱 Bienvenido al Traductor de Plantas Inteligente")
    print("="*70)
    
    try:
        while True:
            # Listar plantas disponibles
            listar_plantas_disponibles()
            
            # Preguntar al usuario si desea generar el dataset CSV
            generar_csv = input("¿Desea generar el dataset CSV con datos simulados? (s/n): ")
            
            if generar_csv.lower() == "s":
                generar_dataset_csv()
            
            # Ejemplo de uso de TraductorPlantaInteligente
            print("\nEjemplo de uso de TraductorPlantaInteligente:")
            config_ejemplo = ConfiguracionPlanta(
                nombre="Ejemplo",
                humedad_min=30.0,
                humedad_max=70.0,
                temperatura_min=15.0,
                temperatura_max=25.0,
                luz_min=20.0,
                luz_max=80.0
            )
            
            traductor_ejemplo = TraductorPlantaInteligente(
                nombre="Planta Ejemplo",
                tipo_planta="General",
                config=config_ejemplo
            )
            
            # Procesar una lectura de ejemplo
            lectura_ejemplo, mensaje_ejemplo = traductor_ejemplo.procesar_lectura()
            print(f"Lectura de ejemplo: Humedad {lectura_ejemplo.humedad_pct}%, "
                  f"Temperatura {lectura_ejemplo.temperatura}°C, Luz {lectura_ejemplo.luz_pct}%")
            print(f"Mensaje de la planta: {mensaje_ejemplo}")
            
            # Preguntar si el usuario desea salir
            salir = input("\n¿Desea salir del programa? (s/n): ")
            if salir.lower() == "s":
                break
    
    except KeyboardInterrupt:
        print("\n\n🌼 Gracias por usar el Traductor de Plantas Inteligente")
        print("   ¡Hasta luego!")
    except Exception as e:
        print(f"\n⚠️  Ocurrió un error inesperado: {e}")
        print("   Por favor, revise los detalles y vuelva a intentar.")
        print("   Si el problema persiste, contacte al soporte técnico.")