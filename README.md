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
- **Matriz de Correlación**: Muestra las correlaciones entre variables.
- **Regresión Paso a Paso**: Ejecuta el algoritmo de selección de variables.

### Visualización
- Gráficas individuales para cada parámetro (Temperatura, OD, pH, DQO, DBO5, SST).
- Filtros por año para análisis temporal.

### Predicción
- Comparación de DBO5 observado vs predicho.
- Análisis de residuales.
- Predicciones específicas para OD y DQO.

### Herramientas Avanzadas
- Tendencia temporal general.
- Simulador de DBO5 para predicciones personalizadas.

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
