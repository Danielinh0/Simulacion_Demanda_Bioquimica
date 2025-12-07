# ProcesoDatos.py
import pandas as pd
import numpy as np

def cargar_limpiar_datos(file_path):
    # Cargar y limpiar datos
    data = pd.read_excel(file_path)
    data_cleaned = data.copy()
    
    # Preservar la columna FECHA y extraer AÑO y MES antes de la conversión
    fecha_column = None
    if 'FECHA' in data_cleaned.columns:
        fecha_column = pd.to_datetime(data_cleaned['FECHA'], dayfirst=True, errors='coerce')
        data_cleaned['AÑO'] = fecha_column.dt.year
        data_cleaned['MES'] = fecha_column.dt.month
        data_cleaned['FECHA_DT'] = fecha_column  # Guardar fecha como datetime
    
    data_cleaned = data_cleaned.replace('<1', np.nan).replace('<10', np.nan)
    
    # Preservar columnas antes de conversión numérica
    año_column = data_cleaned['AÑO'].copy() if 'AÑO' in data_cleaned.columns else None
    mes_column = data_cleaned['MES'].copy() if 'MES' in data_cleaned.columns else None
    fecha_dt_column = data_cleaned['FECHA_DT'].copy() if 'FECHA_DT' in data_cleaned.columns else None
    
    data_cleaned = data_cleaned.apply(pd.to_numeric, errors='coerce')
    
    # Restaurar columnas
    if año_column is not None:
        data_cleaned['AÑO'] = año_column
    if mes_column is not None:
        data_cleaned['MES'] = mes_column
    if fecha_dt_column is not None:
        data_cleaned['FECHA_DT'] = fecha_dt_column
    
    # Quitar filas con valores nulos en columnas relevantes
    data_cleaned = data_cleaned.dropna(subset=['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA', 'DBO5'])
    return data_cleaned

def load_validation_data(file_path):
    # Cargar datos de validación (solo 2012 y 2013)
    data = pd.read_excel(file_path)
    
    # Extraer año de la fecha
    if 'FECHA' in data.columns:
        data['AÑO'] = pd.to_datetime(data['FECHA'], dayfirst=True, errors='coerce').dt.year
    
    validation_data = data[(data['AÑO'] == 2012) | (data['AÑO'] == 2013)]
    validation_data = validation_data.dropna(subset=['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA', 'DBO5'])
    
    return validation_data
