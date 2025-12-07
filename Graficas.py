import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def plot_tss_bod5_relationship(TSS, BOD5):
    """
    Gráfico de la relación lineal entre TSS y BOD5 con R² y predicción fija usando la ecuación obtenida.
    
    :param TSS: Valores de TSS (Sólidos Suspendidos Totales).
    :param BOD5: Valores de BOD5 (Demanda Biológica de Oxígeno).
    """
    # Ajustar modelo de regresión lineal
    TSS = np.array(TSS).reshape(-1, 1)  # Asegurarnos que TSS tiene la forma correcta
    BOD5 = np.array(BOD5)
    
    model = LinearRegression()
    model.fit(TSS, BOD5)

    # Obtener la pendiente (m) y el intercepto (b) de la regresión
    m = model.coef_[0]  # Pendiente
    b = model.intercept_  # Intercepto

    # Mostrar la ecuación obtenida
    print(f"Ecuación de la regresión: BOD5 = {m:.2f} * TSS + {b:.2f}")

    # Predicciones de BOD5 usando la ecuación obtenida
    # Usar la ecuación fija para hacer las predicciones
    BOD5_pred = m * TSS.flatten() + b  # Esto utiliza la fórmula fija

    # Calcular R²
    r2_score = model.score(TSS, BOD5)

    # Generar valores para la línea de regresión
    TSS_range = np.linspace(min(TSS), max(TSS), 500).reshape(-1, 1)
    BOD5_line = m * TSS_range.flatten() + b  # Usar la misma ecuación para la línea de ajuste

    # Crear la gráfica
    plt.figure(figsize=(8, 6))
    plt.scatter(TSS, BOD5, color='blue', alpha=0.7, label='Valores Observados (BOD5)')
    plt.scatter(TSS, BOD5_pred, color='orange', alpha=0.7, label='BOD5 Predicha')  # BOD5 Predicha
    plt.plot(TSS_range, BOD5_line, color='red', linewidth=2, label=f'Línea de Ajuste\n$R^2 = {r2_score:.2f}$')

    # Configuración de la gráfica
    plt.title('Relación Lineal entre TSS y BOD5', fontsize=14)
    plt.xlabel('TSS (Sólidos Suspendidos Totales)', fontsize=12)
    plt.ylabel('BOD5 (Demanda Biológica de Oxígeno)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Mostrar gráfica
    plt.show()

# Ejemplo de datos
TSS = [10, 20, 30, 40, 50]
BOD5 = [2.1, 4.0, 5.8, 7.5, 9.2]

# Llamar a la función
plot_tss_bod5_relationship(TSS, BOD5)