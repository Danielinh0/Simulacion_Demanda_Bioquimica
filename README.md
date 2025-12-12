# Simulación de Demanda Bioquímica de Oxígeno (DBO5)

## Introducción

Este proyecto es un sistema de análisis de regresión lineal múltiple diseñado para calcular y predecir la Demanda Bioquímica de Oxígeno (DBO5) en el Río Atoyac. Utiliza datos históricos de parámetros de calidad del agua como Oxígeno Disuelto (OD), Demanda Química de Oxígeno (DQO), pH, Sólidos Suspendidos Totales (SST) y temperatura para construir modelos predictivos.

## Cómo funciona

El sistema emplea técnicas de regresión lineal múltiple con selección de variables paso a paso (stepwise regression) para identificar los parámetros más significativos que afectan la DBO5. El proceso incluye:

1. **Carga y limpieza de datos**: Los datos se cargan desde archivos Excel y se limpian eliminando valores nulos y outliers.

2. **Análisis estadístico**: Se calcula la matriz de correlación y se realiza regresión paso a paso eliminando variables con p-valores altos.

3. **Modelado predictivo**: Se construyen ecuaciones de regresión como:
   - DBO5 = -6.6283 * OD + 0.3407 * DQO + 21.3075
   - Y otras variaciones según los parámetros disponibles.

4. **Visualización**: Gráficas interactivas para analizar tendencias temporales y comparaciones.

## Opciones del sistema

La interfaz gráfica ofrece las siguientes funcionalidades organizadas en menús:

### Análisis Estadístico
- **Matriz de Correlación**: Genera una tabla o mapa de calor que muestra los coeficientes de correlación de Pearson entre todas las variables ambientales (pH, DQO, OD, SST, temperatura y DBO5). Los valores van de -1 a 1, donde 1 indica correlación positiva perfecta, -1 correlación negativa perfecta, y 0 ninguna correlación lineal. Ayuda a identificar qué variables están más relacionadas con la DBO5 y cuáles podrían ser redundantes en el modelo predictivo.

- **Regresión Paso a Paso**: Ejecuta el algoritmo de selección automática de variables que comienza incluyendo todas las variables predictoras y elimina iterativamente la que tenga el p-valor más alto (menos significativa) en cada ronda, hasta que solo queden variables estadísticamente significativas. Muestra el resumen del modelo para cada ronda, incluyendo coeficientes de regresión, R², R² ajustado, estadísticos F, p-valores individuales y ecuación final. Este proceso construye el modelo predictivo óptimo para DBO5.

### Visualización
- **Gráficas individuales para cada parámetro**: Genera gráficos de líneas que muestran la evolución temporal de cada variable ambiental (Temperatura del agua, Oxígeno Disuelto en mg/L, pH del campo, Demanda Química de Oxígeno total, Demanda Bioquímica de Oxígeno a 5 días, y Sólidos Suspendidos Totales) a lo largo de los meses y años registrados. El eje X representa el tiempo (meses), mientras que el eje Y muestra los valores medidos. Esta visualización permite identificar patrones estacionales, tendencias a largo plazo, picos de contaminación y anomalías en la calidad del agua del río.

- **Filtros por año**: Incluye un menú desplegable que permite seleccionar años específicos (por ejemplo, 2010, 2015) o "Todos los años" para ver datos agregados. Al seleccionar un año, las gráficas se actualizan dinámicamente para mostrar solo los datos de ese período, facilitando comparaciones interanuales y el análisis de cambios en la calidad del agua a través del tiempo.

### Predicción
- **Comparación DBO5 observado vs predicho**: Crea un gráfico de líneas superpuestas que compara los valores reales de DBO5 medidos en el campo con los valores estimados por el modelo de regresión. Una buena superposición indica un modelo preciso; desviaciones grandes sugieren áreas donde el modelo necesita mejora. Incluye leyendas y tooltips para identificar puntos específicos.

- **DBO5 vs Predicción**: Produce un diagrama de dispersión (scatter plot) donde cada punto representa una observación, con el valor observado en el eje X y el predicho en el eje Y. Una línea diagonal de 45 grados sirve como referencia perfecta; puntos por encima de la línea indican subestimaciones del modelo, mientras que puntos por debajo indican sobreestimaciones. Incluye métricas como R² y RMSE en el gráfico.

- **Análisis de residuales**: Muestra los errores del modelo (residuales = observado - predicho) en forma de histograma para verificar la distribución normal, y como gráfico de dispersión contra los valores predichos para comprobar la homoscedasticidad (varianza constante). Ayuda a validar las suposiciones estadísticas del modelo de regresión lineal. *Nota: Requiere ejecutar previamente la "Regresión Paso a Paso" para generar el modelo cuyos residuales se analizarán.*

- **Predicción OD**: Utiliza un modelo de regresión específico entrenado para predecir el Oxígeno Disuelto basado en variables como DQO, pH y temperatura. Muestra la ecuación del modelo, coeficientes, y genera predicciones con intervalos de confianza, útil para estimar niveles de oxígeno en ausencia de mediciones directas.

- **Predicción DQO**: Emplea un modelo de regresión dedicado para estimar la Demanda Química de Oxígeno usando parámetros correlacionados como DBO5, SST y OD. Presenta la ecuación matemática, estadísticas de ajuste, y permite predicciones puntuales con visualización de la relación entre variables predictoras y la DQO estimada.

### Herramientas Avanzadas
- **Tendencia temporal general**: Crea un gráfico compuesto que muestra la evolución conjunta de todos los parámetros normalizados en una sola vista, permitiendo identificar correlaciones temporales entre variables (por ejemplo, cómo aumenta la DBO5 cuando disminuye el OD). Incluye líneas de tendencia y permite zoom para análisis detallado de períodos específicos.

- **Simulador DBO5**: Interfaz interactiva con campos de entrada para cada parámetro (OD, DQO, pH, SST, temperatura), un botón de "Calcular" que aplica la ecuación de regresión en tiempo real, y muestra el valor predicho de DBO5 con intervalo de confianza. Ideal para escenarios hipotéticos, planificación de monitoreo o evaluación de impacto de cambios en la calidad del agua.

## Instrucciones para correr el proyecto

### Prerrequisitos
- Python 3.x instalado
- Librerías necesarias: scikit-learn, statsmodels, matplotlib, openpyxl

### Instalación
```bash
pip install -U scikit-learn
pip install statsmodels
pip install matplotlib
pip install openpyxl
```

### Ejecución
1. Coloca tu archivo de datos Excel en el directorio del proyecto.
2. Ejecuta el programa principal:
```bash
python Main.py
```
3. En la interfaz, haz clic en "Cargar Datos (Excel)" y selecciona tu archivo.
4. Explora las diferentes opciones del menú lateral.

### Formato de datos
El archivo Excel debe contener las siguientes columnas:
- FECHA
- pH_CAMPO
- DQO_TOT
- OD_mg/L
- SST
- TEMP_AGUA
- DBO5
