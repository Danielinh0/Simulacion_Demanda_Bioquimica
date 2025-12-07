#Analisis de Regresion.py
import numpy as np
import statsmodels.api as sm
import pandas as pd
from sklearn.linear_model import LinearRegression

def run_regression_and_display_results(X, y, round_name):
    model = sm.OLS(y, X).fit()
    print(f"\nResultados de {round_name}:")
    # Obtener valores generales del modelo
    r = model.rsquared ** 0.5  # R
    r_squared = model.rsquared  # R^2
    std_error = model.bse.mean()  # Error estándar promedio
    observations = int(model.nobs)  # Número de observaciones
    significance = model.f_pvalue  # Significancia del modelo (F-statistic p-value)

    # Coeficientes individuales
    coef = model.params
    p_values = model.pvalues

    # Crear lista con la información deseada
    elements = [
        ("R", r, ''),
        ("R^2", r_squared, ''),
        ("Error estandar", std_error, ''),
        ("Observaciones", observations, ''),
        ("Significancia", significance, ''),
        ("Constante", p_values.get("const", 'N/A'), '')
    ]
    
    # Agregar p-valores de cada variable incluida en el modelo
    variables = ["pH_CAMPO", "DQO_TOT", "OD_mg/L", "TEMP_AGUA"]
    for var in variables:
        elements.append((var, p_values.get(var, 'N/A'), ''))

    # Crear DataFrame con formato personalizado
    df_results = pd.DataFrame(elements, columns=["Elemento", "Valor", ""])

    # Formato condicional para cada valor en la columna 'Valor'
    def format_value(val):
        if isinstance(val, (int, float)):
            if abs(val) < 1e-6:  # Notación científica para valores muy pequeños
                return f"{val:.2e}"
            elif val.is_integer():  # Sin decimales si el número es entero
                return str(int(val))
            else:  # Hasta 6 decimales para otros números
                return f"{val:.6f}"
        return val  # En caso de ser 'N/A' u otro texto

    # Aplicar formato a la columna 'Valor'
    df_results['Valor'] = df_results['Valor'].apply(format_value)

    print(df_results)
    
    return model
def stepwise_regression(X, y):
    X = sm.add_constant(X)

    # Ronda 1: Eliminando 'SST'
    X_ronda_1 = X.drop(columns=['SST'])
    model_ronda_1 = run_regression_and_display_results(X_ronda_1, y, "Ronda 1")

    # Ronda 2: Eliminando la variable con el P>|t| más alto en la Ronda 1
    var_to_remove_ronda_2 = model_ronda_1.pvalues[1:].idxmax()  # Excluye el p-valor del intercepto
    X_ronda_2 = X_ronda_1.drop(columns=[var_to_remove_ronda_2])
    model_ronda_2 = run_regression_and_display_results(X_ronda_2, y, "Ronda 2")

    # Ronda 3: Eliminando la variable con el P>|t| más alto en la Ronda 2
    var_to_remove_ronda_3 = model_ronda_2.pvalues[1:].idxmax()  # Excluye el p-valor del intercepto
    X_ronda_3 = X_ronda_2.drop(columns=[var_to_remove_ronda_3])
    model_ronda_3 = run_regression_and_display_results(X_ronda_3, y, "Ronda 3")
    print(model_ronda_3.summary())

    return model_ronda_3  # Devuelve el último modelo
def calculate_correlation_matrix(data, target_column='DBO5'):
    """
    Calcula y devuelve la matriz de correlación de Pearson entre las variables seleccionadas
    y la variable objetivo (DBO5).
    """
    # Seleccionar las variables específicas para la correlación
    selected_columns = ['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA', target_column]
    correlation_matrix = data[selected_columns].corr(method='pearson')
    
    # Imprimir la matriz de correlación solo con las variables seleccionadas
    print("\nMatriz de correlación de Pearson entre las variables seleccionadas y", target_column, ":")
    print(correlation_matrix[[target_column]].sort_values(by=target_column, ascending=False))
    
    return correlation_matrix
def calcular_BOD5(OD, DQO):
    """
    Calcula BOD5 usando la ecuación: BOD5 = 0.498992 * TSS + 0.052154 * OD_mg/L + 1013197
    """
    return -6.6283 * OD + 0.3407 * DQO + 21.3075
def calcular_BOD5_OD(OD):
    """
    Calcula BOD5 usando la ecuación: BOD5 = 0.498992 * TSS + 0.052154 * OD_mg/L + 1013197
    """
    return 0.3597 * OD  + 1.0979
def prediccion_cod(COD, BOD5_observado):
    model = LinearRegression()  # Crear el modelo de regresión lineal
    model.fit(COD.reshape(-1, 1), BOD5_observado)  # Ajustar el modelo a los datos
    COD_range = np.linspace(min(COD), max(COD), 500).reshape(-1, 1)
    BOD5_predicho = model.predict(COD.reshape(-1, 1))  # Predicción de los valores BOD5
    BOD5_linea = model.predict(COD_range)  # Predicción de la línea de regresión
    
    return model, BOD5_predicho, BOD5_linea
def prediccion_sst(COD, BOD5_observado, COD_range):
    model = LinearRegression()  # Crear el modelo de regresión lineal
    model.fit(COD.reshape(-1, 1), BOD5_observado)  # Ajustar el modelo a los datos
    
    BOD5_predicho = model.predict(COD.reshape(-1, 1))  # Predicción de los valores BOD5
    BOD5_linea = model.predict(COD_range)  # Predicción de la línea de regresión
    
    return model, BOD5_predicho, BOD5_linea
def stepwise_regression_dqo(X, y):
    X = sm.add_constant(X)

    # Ronda 1: Eliminando 'SST'
    X_ronda_1 = X.drop(columns=['SST'])
    model_ronda_1 = run_regression_and_display_results(X_ronda_1, y, "Ronda 1")

    # Ronda 2: Eliminando la variable con el P>|t| más alto en la Ronda 1
    var_to_remove_ronda_2 = model_ronda_1.pvalues[1:].idxmax()  # Excluye el p-valor del intercepto
    X_ronda_2 = X_ronda_1.drop(columns=[var_to_remove_ronda_2])
    model_ronda_2 = run_regression_and_display_results(X_ronda_2, y, "Ronda 2")

    # Ronda 3: Eliminando la variable con el P>|t| más alto en la Ronda 2
    var_to_remove_ronda_3 = model_ronda_2.pvalues[1:].idxmax()  # Excluye el p-valor del intercepto
    X_ronda_3 = X_ronda_2.drop(columns=[var_to_remove_ronda_3])
    model_ronda_3 = run_regression_and_display_results(X_ronda_3, y, "Ronda 3")
    print(model_ronda_3.summary())

    return model_ronda_3  # Devuelve el último modelo
def stepwise_regression_od(X, y):
    X = sm.add_constant(X)
    model_ronda_1 = run_regression_and_display_results(X, y, "Ronda 1")
    print(model_ronda_1.summary())

    return model_ronda_1  # Devuelve el último modelo
