# Guía de Uso del Dashboard de Plantas

## Descripción

El dashboard ahora utiliza los **datos reales de 960 plantas** cargados desde el archivo `plantas.json` en lugar de datos simulados genéricos.

## Cambios Realizados

### Antes (Demo)
- Generaba datos simulados genéricos
- Usaba una planta ficticia "Cactus del Desierto (Demo)"
- No utilizaba los datos del JSON

### Ahora (Datos Reales)
- Carga datos desde `plantas.json` (960 plantas)
- Genera datos realistas basados en los parámetros específicos de cada planta
- Muestra información precisa de temperatura, humedad y luz según la especie

## Formas de Usar

### 1. Modo Interactivo (Recomendado)
```bash
python dashboard_plantas.py
```
El programa te hará las siguientes preguntas:
1. **¿Qué planta deseas visualizar?** - Escribe el nombre exacto (ej: "Acacia")
2. **¿Cuántos días de datos deseas simular?** - Opciones recomendadas: 7, 15, 30 (puedes usar cualquier número entre 1 y 365)
3. **¿Deseas guardar el dashboard como imagen?** - s/n (default: n)

### 2. Modo Línea de Comandos
```bash
python dashboard_plantas.py NombrePlanta [dias] [guardar]
```

**Ejemplos:**
```bash
# Dashboard de Acacia con 30 días
python dashboard_plantas.py Acacia

# Dashboard de Airplant con 60 días
python dashboard_plantas.py Airplant 60

# Dashboard de Aloe Vera con 45 días y guardar imagen
python dashboard_plantas.py "Aloe Vera" 45 true
```

### 3. Ejemplo de Sesión Interactiva
```
python dashboard_plantas.py

================================================================================
DASHBOARD CON DATOS REALES DE PLANTAS
================================================================================

Ejemplos de plantas disponibles:
  - Acacia, Airplant, Alpine Buttercup
  - Alumroot, American Globeflower, Angelwing Jasmine
  - Aaron's Beard, Absaroka Range Beardtongue

Tip: Tambien puedes usar: python dashboard_plantas.py NombrePlanta [dias] [guardar]

Ingrese el nombre de la planta que desea visualizar: Acacia
Ingrese la cantidad de dias de datos a simular (7, 15, 30): 15
Desea guardar el dashboard como imagen? (s/n, default: n): n

Generando dashboard para 'Acacia' con 15 dias de datos...
[Se muestra el dashboard con gráficos]

OK - Dashboard generado exitosamente!
```

### 4. Importar en tu propio script
```python
from dashboard_plantas import generar_dashboard_con_datos

# Generar dashboard para una planta específica
generar_dashboard_con_datos("Acacia", dias=30, guardar=False)
```

## Plantas Disponibles

El sistema tiene **960 plantas** disponibles. Algunos ejemplos:

- Acacia
- Airplant
- Alpine Buttercup
- Alumroot
- American Globeflower
- Angelwing Jasmine
- Annual Ragweed
- Y muchas más...

Para ver la lista completa de plantas disponibles, ejecuta:
```bash
python -c "from planta_config import listar_nombres_plantas; print('\\n'.join(listar_nombres_plantas()))"
```

## Características del Dashboard

El dashboard generado incluye **4 gráficos**:

1. **Evolución de Humedad (30 días)**
   - Muestra el patrón de riego realista
   - Incluye rangos óptimos específicos de la planta
   - Indica el promedio de humedad

2. **Temperatura y Niveles de Luz**
   - Gráfico dual con dos ejes Y
   - Variaciones diarias y semanales
   - Rangos óptimos por especie

3. **Distribución de Estados de Salud**
   - Óptimo, Aceptable, Crítico
   - Basado en análisis de múltiples parámetros
   - Porcentaje de días en cada estado

4. **Comparación Real vs Óptimo**
   - Compara promedios reales con ideales
   - Para humedad, temperatura y luz
   - Visualización clara de desviaciones

## Datos Simulados Realistas

Aunque los datos de monitoreo son simulados (porque representan 30 días de sensores), se generan de forma realista basándose en:

- **Humedad**: Patrón de riego según frecuencia_riego_dias de cada planta
- **Temperatura**: Variación sinusoidal semanal + ruido diario
- **Luz**: Variación estacional mensual + ruido aleatorio

Todos los valores se mantienen dentro de los rangos específicos de cada planta del JSON.

## Guardar Dashboards

Para guardar el dashboard como imagen PNG:

```bash
python dashboard_plantas.py Acacia 30 true
```

O en modo interactivo, usa la función directamente:
```python
from dashboard_plantas import generar_dashboard_con_datos

generar_dashboard_con_datos(
    "Acacia",
    dias=30,
    guardar=True,
    nombre_archivo="mi_dashboard_acacia.png"
)
```

## Solución de Problemas

### Error: "No se encontró la planta"
- Verifica que el nombre esté escrito correctamente
- Los nombres son sensibles a mayúsculas/minúsculas
- Usa la lista de plantas disponibles para confirmar

### El dashboard no se muestra
- Asegúrate de tener matplotlib instalado: `pip install matplotlib numpy`
- En algunos entornos, puede ser necesario usar modo no interactivo

### Caracteres extraños en la consola
- Esto es normal en Windows con caracteres especiales
- No afecta la funcionalidad del dashboard
