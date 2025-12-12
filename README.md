# Simulación de Demanda Bioquímica de Oxígeno (DBO)

## Descripción
Proyecto de simulación en Python que implementa un modelo de regresión lineal múltiple para estimar la Demanda Bioquímica de Oxígeno (DBO) en muestras de agua. Permite preparar datos, entrenar y evaluar un modelo, guardar/cargar el modelo entrenado y realizar predicciones sobre nuevos conjuntos de datos.

## Introducción
La DBO (Demanda Bioquímica de Oxígeno) mide la cantidad de oxígeno que requieren los microorganismos aeróbicos para descomponer la materia orgánica de una muestra de agua. Este proyecto implementa un enfoque de regresión lineal múltiple para relacionar variables explicativas (por ejemplo: temperatura, pH, sólidos totales, nutrientes) con la DBO y obtener estimaciones útiles para monitoreo de calidad de agua y estudios ambientales.

## Metodología y flujo de trabajo
- Carga y preparación de datos (CSV).
- Preprocesamiento: limpieza, tratamiento de valores faltantes, codificación de categóricas, escalado (opcional).
- Ingeniería de características y selección de variables.
- Entrenamiento de un modelo de regresión lineal múltiple (scikit-learn).
- Evaluación con métricas como R², MAE y RMSE.
- Persistencia del modelo (pickle / joblib) y uso para predicciones.

## Opciones y funcionalidades
- Entrenamiento del modelo con tus datos.
- Evaluación y generación de métricas.
- Guardado y carga de modelos entrenados.
- Predicción sobre nuevos datos en lote.
- Parámetros de preprocesamiento configurables: imputación, normalización/estandarización, selección de variables.
- Soporte para ejecutar desde scripts o notebooks (dependiendo de la estructura del repo).

Si los nombres de los scripts en el repositorio difieren (por ejemplo `train.py`, `predict.py`), adapta los comandos según corresponda.

## Requisitos
- Python 3.8+
- Entorno virtual recomendado (venv, conda)

Dependencias (todas las librerías necesarias para ejecutar los scripts del proyecto):
- numpy
- pandas
- scikit-learn
- joblib
- statsmodels
- matplotlib
- openpyxl
- mplcursors

Instalación rápida:
- Si existe requirements.txt:
  pip install -r requirements.txt
- Si no existe, instala todas las dependencias con un solo comando:
  pip install numpy pandas scikit-learn joblib statsmodels matplotlib openpyxl mplcursors

## Estructura sugerida del repositorio
- data/                - archivos CSV de entrada
- notebooks/           - análisis exploratorio y visualizaciones
- src/ o scripts/      - scripts de entrenamiento/evaluación/predicción
- models/              - modelos guardados (.pkl / .joblib)
- results/             - salidas, predicciones y reportes
- README.md

Ajusta según la estructura real del repositorio.

## Instrucciones para ejecutar (guía general)

1. Clonar el repositorio:
   git clone https://github.com/Danielinh0/Simulacion_Demanda_Bioquimica.git
   cd Simulacion_Demanda_Bioquimica

2. Crear y activar un entorno virtual (opcional):
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt
   (o instalar manualmente: pip install numpy pandas scikit-learn joblib statsmodels matplotlib openpyxl mplcursors)

4. Preparar datos:
   - Coloca los CSV en la carpeta data/.
   - Debe existir una columna objetivo con la DBO (por ejemplo `DBO` o `dbo`) y columnas predictoras.
   - Asegúrate de revisar y limpiar valores faltantes o anómalos.

5. Entrenar el modelo:
   - Ejemplo genérico (ajusta según la estructura del repo):
     python src/train.py --data data/tu_dataset.csv --target DBO --output models/dbo_model.pkl
   - Alternativamente, ejecutar un notebook de entrenamiento en notebooks/.

6. Evaluar el modelo:
   - Ejemplo:
     python src/evaluate.py --model models/dbo_model.pkl --data data/tu_dataset.csv
   - Genera métricas R², MAE, RMSE y reportes opcionales.

7. Predecir con nuevos datos:
   - Ejemplo:
     python src/predict.py --model models/dbo_model.pkl --data data/nuevos_datos.csv --output results/predicciones.csv

## Formato de los datos
- Archivo CSV con encabezados.
- Columna objetivo (DBO) numérica.
- Columnas predictoras numéricas o categóricas. Las categóricas deben convertirse (one-hot o label encoding) durante el preprocesamiento.
- Evitar filas con valores no numéricos en columnas previstas para modelado sin tratarlas primero.

## Buenas prácticas
- Realizar validación cruzada para estimaciones robustas.
- Revisar supuestos de la regresión lineal: linealidad, homocedasticidad, independencia y multicolinealidad.
- Inspeccionar residuos para detectar sesgos o patrones no modelados.
- Normalizar/estandarizar variables cuando sea apropiado.
- Documentar las transformaciones aplicadas a los datos para reproducibilidad.

## Ejemplo de pipeline mínimo (pseudocódigo)
1. Cargar CSV (pandas).
2. Imputar valores faltantes (media/mediana o técnicas avanzadas).
3. Codificar variables categóricas.
4. Dividir en train/test (por ejemplo train_test_split).
5. Escalar variables si aplica (StandardScaler o MinMaxScaler).
6. Entrenar LinearRegression.
7. Evaluar con test y guardar modelo con joblib.dump().

## Contribuciones
Si deseas contribuir:
- Abre un issue describiendo la mejora o bug.
- Crea una rama por feature y abre un pull request con descripción clara y ejemplos.
- Añade pruebas o notebooks de demostración cuando sea posible.

## Licencia
Añade aquí la licencia deseada (por ejemplo MIT). Si no hay licencia especificada, contacta al autor para permiso de uso.

## Contacto
Autor: Danielinh0
Repositorio: https://github.com/Danielinh0/Simulacion_Demanda_Bioquimica