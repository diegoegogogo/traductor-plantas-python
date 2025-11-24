# Dashboard de Visualización para Traductor de Plantas 📊

Sistema de graficación avanzada para monitoreo de plantas con múltiples métricas y análisis visuales.

## 🎯 Características

El dashboard incluye **4 gráficos simultáneos**:

1. **Evolución de Humedad (30 días)**
   - Línea temporal con lecturas diarias
   - Banda de rango óptimo sombreada
   - Línea de promedio
   - Identificación visual de problemas

2. **Temperatura y Luz**
   - Doble eje Y para dos métricas simultáneas
   - Tendencias temporales
   - Rangos óptimos marcados

3. **Distribución de Estados**
   - Gráfico de barras con clasificación de días
   - Estados: Óptimo, Aceptable, Crítico
   - Porcentajes calculados automáticamente

4. **Comparación Real vs Óptimo**
   - Gráfico comparativo de barras
   - Valores promedio medidos vs ideales
   - Para humedad, temperatura y luz

## 📦 Instalación

### Requisitos previos

```bash
pip install matplotlib numpy pandas
```

### Archivos necesarios

- `dashboard_plantas.py` - Módulo principal del dashboard
- `ejemplo_uso_dashboard.py` - Ejemplos de uso
- `README_DASHBOARD.md` - Esta documentación

## 🚀 Uso Rápido

### 1. Demo Rápida

```bash
python dashboard_plantas.py
```

Esto ejecutará una demostración con datos simulados realistas.

### 2. Uso Básico en tu código

```python
from dashboard_plantas import generar_dashboard

# Tus datos (30 días de lecturas)
humedad = [55.2, 54.8, 53.9, ..., 52.1]  # 30 valores
temperatura = [22.5, 23.1, 21.8, ..., 22.9]  # 30 valores
luz = [65.3, 68.2, 70.1, ..., 67.5]  # 30 valores

# Generar dashboard
generar_dashboard(
    datos_humedad=humedad,
    datos_temperatura=temperatura,
    datos_luz=luz,
    nombre_planta="Mi Rosa del Jardín",
    humedad_optima=(50, 75),
    temperatura_optima=(18, 26),
    luz_optima=(60, 85)
)
```

### 3. Guardar como imagen

```python
generar_dashboard(
    datos_humedad=humedad,
    datos_temperatura=temperatura,
    datos_luz=luz,
    nombre_planta="Cactus",
    guardar=True,
    nombre_archivo="mi_dashboard.png"
)
```

### 4. Desde archivo CSV

```python
from dashboard_plantas import generar_dashboard_desde_csv

generar_dashboard_desde_csv(
    archivo_csv="dataset_plantas_960.csv",
    nombre_planta="Acacia",
    guardar=True
)
```

## 📚 Ejemplos Completos

Ejecuta el archivo de ejemplos interactivo:

```bash
python ejemplo_uso_dashboard.py
```

Esto te mostrará un menú con 5 opciones:
1. Dashboard con datos simulados
2. Dashboard desde archivo CSV
3. Dashboard con datos personalizados
4. Comparar múltiples plantas
5. Demo rápida

## 🔧 Integración con tu proyecto existente

### Opción A: Importar en tu código principal

```python
# En tu archivo principal (Traductor de plantas.py)
from dashboard_plantas import generar_dashboard

# Después de recolectar datos de sensores...
historial_humedad = [lectura1, lectura2, ..., lectura30]
historial_temp = [temp1, temp2, ..., temp30]
historial_luz = [luz1, luz2, ..., luz30]

# Generar visualización
generar_dashboard(
    datos_humedad=historial_humedad,
    datos_temperatura=historial_temp,
    datos_luz=historial_luz,
    nombre_planta=config_planta.nombre,
    humedad_optima=(config_planta.humedad_min, config_planta.humedad_max),
    temperatura_optima=(config_planta.temperatura_min, config_planta.temperatura_max),
    luz_optima=(config_planta.luz_min, config_planta.luz_max)
)
```

### Opción B: Agregar al sistema de reportes

```python
class TraductorPlantas:
    # ... tu código existente ...

    def generar_reporte_visual(self):
        """Genera dashboard visual de los últimos 30 días"""
        from dashboard_plantas import generar_dashboard

        if len(self.historial) < 30:
            print("Necesitas al menos 30 lecturas para generar el dashboard")
            return

        # Extraer datos del historial
        humedad = [h.humedad_pct for h in self.historial[-30:]]
        temp = [h.temperatura for h in self.historial[-30:]]
        luz = [h.luz_pct for h in self.historial[-30:]]

        # Generar dashboard
        generar_dashboard(
            datos_humedad=humedad,
            datos_temperatura=temp,
            datos_luz=luz,
            nombre_planta=self.config.nombre,
            humedad_optima=(self.config.humedad_min, self.config.humedad_max),
            temperatura_optima=(self.config.temperatura_min, self.config.temperatura_max),
            luz_optima=(self.config.luz_min, self.config.luz_max),
            guardar=True
        )
```

## 📊 Personalización

### Cambiar colores

Edita el diccionario `COLORES` en `dashboard_plantas.py`:

```python
COLORES = {
    'primario': '#2ecc71',      # Verde para humedad
    'secundario': '#3498db',    # Azul para luz
    'peligro': '#e74c3c',       # Rojo para temperatura
    'advertencia': '#f39c12',   # Naranja para advertencias
    'info': '#9b59b6',          # Púrpura para info
    'exito': '#27ae60',         # Verde oscuro para éxito
    'neutro': '#95a5a6'         # Gris para neutro
}
```

### Cambiar resolución de imagen

```python
generar_dashboard(
    ...,
    guardar=True
)

# Luego modifica en el código la línea:
# plt.savefig(nombre_archivo, dpi=300, ...)
# Cambia 300 por 150 (menor calidad) o 600 (mayor calidad)
```

## 🐛 Solución de Problemas

### Error: "No module named 'matplotlib'"

```bash
pip install matplotlib
```

### Error: "No module named 'numpy'"

```bash
pip install numpy
```

### Dashboard no se muestra

- Verifica que tienes al menos 30 datos
- En Windows, asegúrate de tener un backend de matplotlib configurado
- Prueba con `guardar=True` para generar una imagen en lugar de mostrarla

### Las listas tienen longitudes diferentes

El dashboard automáticamente recorta los datos al mínimo común. Pero es mejor verificar:

```python
print(f"Humedad: {len(datos_humedad)} valores")
print(f"Temp: {len(datos_temperatura)} valores")
print(f"Luz: {len(datos_luz)} valores")
```

## 📈 Interpretación de Resultados

### Gráfico 1: Evolución de Humedad
- **Línea dentro de banda verde**: Planta en condiciones óptimas
- **Línea debajo de banda**: Necesita riego
- **Línea arriba de banda**: Exceso de agua (riesgo de pudrición)

### Gráfico 2: Temperatura y Luz
- **Bandas sombreadas**: Rangos óptimos
- **Picos fuera de rango**: Identificar momentos problemáticos

### Gráfico 3: Distribución de Estados
- **Óptimo (verde)**: Planta en perfecto estado
- **Aceptable (amarillo)**: Un parámetro fuera de rango
- **Crítico (rojo)**: Dos o más parámetros fuera de rango

### Gráfico 4: Comparación Real vs Óptimo
- **Barras similares**: Condiciones cercanas al ideal
- **Gran diferencia**: Ajusta las condiciones de cultivo

## 🎨 Ejemplo de Dashboard Generado

El dashboard se verá así:

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard de Monitoreo: Mi Planta                      │
├──────────────────────┬──────────────────────────────────┤
│ Evolución Humedad    │  Temperatura y Luz              │
│ (línea + banda)      │  (dos ejes Y)                   │
├──────────────────────┼──────────────────────────────────┤
│ Distribución Estados │  Comparación Real vs Óptimo     │
│ (barras)             │  (barras comparativas)          │
└──────────────────────┴──────────────────────────────────┘
```

## 🤝 Contribuir

Para mejorar el dashboard:

1. Abre `dashboard_plantas.py`
2. Busca la función que quieres modificar
3. Realiza tus cambios
4. Prueba con `python dashboard_plantas.py`

## 📝 Notas

- Los dashboards se generan en alta resolución (300 DPI por defecto)
- Compatible con Windows, Linux y macOS
- Los archivos PNG generados son ideales para reportes e informes
- Puedes ejecutar múltiples dashboards en secuencia

## 📞 Soporte

Si tienes problemas:

1. Verifica que todas las dependencias estén instaladas
2. Revisa los ejemplos en `ejemplo_uso_dashboard.py`
3. Ejecuta la demo con `python dashboard_plantas.py`
4. Verifica que tus datos tengan el formato correcto (listas de números)

## 🔮 Próximas Mejoras

Ideas para futuras versiones:

- [ ] Dashboard interactivo con Plotly
- [ ] Exportar a PDF con múltiples páginas
- [ ] Animaciones de evolución temporal
- [ ] Comparación entre múltiples plantas en un solo dashboard
- [ ] Predicciones futuras con ML
- [ ] Alertas automáticas por email/SMS

---

**Autor**: Sistema de Monitoreo de Plantas
**Versión**: 1.0
**Fecha**: 2025
