# Dashboard Integrado con Sistema JSON

## ✅ Integración Completada

El módulo `dashboard_plantas.py` ahora está completamente integrado con el sistema JSON, permitiendo generar dashboards para cualquiera de las 960 plantas disponibles con solo especificar el nombre.

---

## 🎯 Nueva Función: `generar_dashboard_con_datos()`

### Descripción

Esta función simplifica enormemente la generación de dashboards al:
1. Buscar automáticamente la planta en la base de datos JSON
2. Generar datos simulados realistas basados en los parámetros de la planta
3. Crear un dashboard completo con 4 gráficos de análisis

### Firma

```python
def generar_dashboard_con_datos(
    nombre: str,
    dias: int = 30,
    guardar: bool = False,
    nombre_archivo: Optional[str] = None
) -> None
```

### Parámetros

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `nombre` | `str` | - | Nombre de la planta (ej: "Acacia", "Monstera") |
| `dias` | `int` | 30 | Número de días de datos a simular |
| `guardar` | `bool` | False | Si True, guarda la imagen en lugar de mostrarla |
| `nombre_archivo` | `str` | None | Nombre del archivo para guardar |

---

## 📊 Generación de Datos Realistas

La función genera datos simulados que siguen patrones realistas:

### 1. **Humedad del Suelo**
- **Patrón de riego**: Simula ciclos de riego basados en `frecuencia_riego_dias`
- **Decaimiento gradual**: La humedad disminuye entre riegos
- **Variación**: Usa `humedad_desviacion` para añadir ruido realista
- **Rango**: Respeta `humedad_min` y `humedad_max`

### 2. **Temperatura**
- **Variación semanal**: Ciclo sinusoidal de 7 días
- **Ruido diario**: Variaciones aleatorias pequeñas
- **Rango**: Entre `temperatura_min` y `temperatura_max` (±2°C)

### 3. **Luz**
- **Variación estacional**: Ciclo sinusoidal de 30 días
- **Ruido**: Variaciones aleatorias moderadas
- **Rango**: Entre `luz_min` y `luz_max` (±5%)

---

## 🚀 Uso

### Ejemplo 1: Dashboard Simple

```python
from dashboard_plantas import generar_dashboard_con_datos

# Generar dashboard para Acacia (30 días, mostrar en pantalla)
generar_dashboard_con_datos("Acacia")
```

### Ejemplo 2: Más Días de Datos

```python
# Generar dashboard con 60 días de datos
generar_dashboard_con_datos("Alpine Buttercup", dias=60)
```

### Ejemplo 3: Guardar en Archivo

```python
# Generar y guardar dashboard
generar_dashboard_con_datos(
    "Aaron's Beard",
    dias=30,
    guardar=True,
    nombre_archivo="mi_planta.png"
)
```

### Ejemplo 4: Desde Línea de Comandos

```bash
# Usando el script de ejemplo
python ejemplo_dashboard_con_planta.py "Acacia"

# Modo interactivo
python ejemplo_dashboard_con_planta.py --interactivo
```

---

## 📋 Script de Ejemplo Completo

Se incluye [`ejemplo_dashboard_con_planta.py`](ejemplo_dashboard_con_planta.py) que demuestra:

1. **Ejemplos predefinidos**: Genera dashboards para varias plantas
2. **Modo interactivo**: Permite al usuario elegir plantas y configurar opciones
3. **Validación**: Verifica que la planta existe antes de generar
4. **Sugerencias**: Muestra plantas similares si hay un error de tipeo

### Ejecutar ejemplos:

```bash
# Ejemplos predefinidos
python ejemplo_dashboard_con_planta.py

# Planta específica
python ejemplo_dashboard_con_planta.py Acacia

# Modo interactivo
python ejemplo_dashboard_con_planta.py --interactivo
```

---

## 🔄 Comparación: Antes vs Ahora

### ❌ **ANTES** (Líneas 324-382 - `generar_dashboard_desde_csv`)

**Problemas:**
- ❌ Requiere archivo CSV externo
- ❌ Solo funciona con datos pre-generados
- ❌ Necesita pandas
- ❌ Datos solo de humedad (temperatura y luz aleatorios)
- ❌ No usa los parámetros reales de la planta

```python
# Método antiguo (NO RECOMENDADO)
generar_dashboard_desde_csv(
    "plantas_humedad_30dias.csv",
    "Acacia",
    guardar=True
)
```

### ✅ **AHORA** (Nueva función integrada)

**Ventajas:**
- ✅ Usa directamente la base de datos JSON (960 plantas)
- ✅ Genera datos realistas en tiempo real
- ✅ No requiere archivos externos
- ✅ Usa todos los parámetros de la planta
- ✅ Datos coherentes de humedad, temperatura y luz
- ✅ Patrones de riego realistas

```python
# Método nuevo (RECOMENDADO)
generar_dashboard_con_datos("Acacia", dias=30)
```

---

## 📁 Estructura de Archivos

```
Traductore de plantas/
│
├── plantas.json                        # Base de datos (960 plantas)
├── planta_config.py                    # Módulo de carga
├── dashboard_plantas.py                # Módulo de dashboards (ACTUALIZADO)
├── ejemplo_dashboard_con_planta.py     # Script de ejemplo
│
├── Traductor de plantas.py             # Sistema principal 1
├── Proyecto traductor de plantas.py    # Sistema principal 2
│
└── README_DASHBOARD_INTEGRADO.md       # Esta documentación
```

---

## 🔧 Integración Técnica

### Importación

```python
# dashboard_plantas.py
from planta_config import buscar_planta
```

**Ventajas de usar `planta_config.py`:**
- ✅ Módulo dedicado para gestión de plantas
- ✅ Cache LRU para máximo rendimiento
- ✅ Funciones de búsqueda optimizadas
- ✅ Independiente de otros módulos
- ✅ Fácil de mantener

**Por qué NO importar de "Proyecto traductor de plantas.py":**
- ❌ Nombre con espacios (difícil de importar)
- ❌ Archivo grande (47 KB)
- ❌ Dependencias innecesarias
- ❌ Acoplamiento alto

---

## 📊 Dashboard Generado

El dashboard incluye 4 gráficos:

### 1. Evolución de Humedad (30 días)
- Línea de humedad medida
- Banda de rango óptimo
- Línea de promedio
- Patrón de riego visible

### 2. Temperatura y Luz
- Dos ejes Y para temperatura y luz
- Bandas de rangos óptimos
- Variación temporal clara

### 3. Distribución de Estados
- Barras: Óptimo / Aceptable / Crítico
- Porcentajes de días en cada estado
- Colores intuitivos

### 4. Comparación Real vs Óptimo
- Barras comparativas
- Humedad / Temperatura / Luz
- Valores numéricos visibles

---

## 💡 Casos de Uso

### 1. **Análisis de Planta Específica**
```python
# Ver cómo se comportaría una planta en condiciones normales
generar_dashboard_con_datos("Monstera", dias=60)
```

### 2. **Comparar Plantas**
```python
# Generar dashboards de varias plantas para comparar
for planta in ["Cactus", "Helecho", "Suculenta"]:
    generar_dashboard_con_datos(planta, guardar=True, nombre_archivo=f"dashboard_{planta}.png")
```

### 3. **Planificación de Cuidados**
```python
# Ver patrón de riego de una planta
planta = buscar_planta("Acacia")
print(f"Riego cada {planta.frecuencia_riego_dias} días")
generar_dashboard_con_datos("Acacia", dias=30)
```

### 4. **Documentación Visual**
```python
# Crear imágenes para documentación
from planta_config import obtener_plantas_por_tipo

plantas_interior = obtener_plantas_por_tipo("General/Interior")
for p in plantas_interior[:5]:
    generar_dashboard_con_datos(
        p.nombre,
        guardar=True,
        nombre_archivo=f"docs/plantas/{p.nombre.replace(' ', '_')}.png"
    )
```

---

## 🎨 Personalización

Si necesitas personalizar los colores o estilos, puedes modificar el diccionario `COLORES`:

```python
# En dashboard_plantas.py
COLORES = {
    'primario': '#2ecc71',      # Verde (líneas principales)
    'secundario': '#3498db',    # Azul (datos secundarios)
    'peligro': '#e74c3c',       # Rojo (temperaturas altas)
    'advertencia': '#f39c12',   # Naranja (advertencias)
    'info': '#9b59b6',          # Morado (información)
    'exito': '#27ae60',         # Verde oscuro (óptimo)
    'neutro': '#95a5a6'         # Gris (neutral)
}
```

---

## ✅ Ventajas del Sistema Integrado

| Aspecto | Beneficio |
|---------|-----------|
| **Facilidad de uso** | Solo necesitas el nombre de la planta |
| **Precisión** | Datos basados en parámetros reales de la planta |
| **Realismo** | Patrones de riego y variación natural |
| **Escalabilidad** | Funciona con las 960 plantas disponibles |
| **Rendimiento** | Cache LRU para cargas rápidas |
| **Mantenibilidad** | Código limpio y bien organizado |

---

## 🔮 Próximas Mejoras Sugeridas

1. **Integración con datos reales**: Leer de sensores IoT
2. **Comparación múltiple**: Mostrar varios dashboards en una sola figura
3. **Alertas visuales**: Resaltar días críticos
4. **Exportación de datos**: Guardar datos simulados en CSV
5. **Predicciones**: Predecir próximo riego necesario

---

## 📝 Resumen

- ✅ **Dashboard integrado con sistema JSON**
- ✅ **Función simplificada `generar_dashboard_con_datos()`**
- ✅ **Datos realistas basados en parámetros de planta**
- ✅ **960 plantas disponibles**
- ✅ **Script de ejemplo completo**
- ✅ **Documentación completa**

**La integración está completa y lista para usar. Puedes generar dashboards profesionales para cualquier planta con una sola línea de código.**

---

**Fecha**: 2025-11-22
**Autor**: Sistema de Traductor de Plantas
**Versión**: 2.0 (Integrado con JSON)
