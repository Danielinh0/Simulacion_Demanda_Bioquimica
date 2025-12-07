# Visualizacion.py - Versión con tooltips interactivos
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from AnalisisRegresion import calcular_BOD5_OD, stepwise_regression_dqo, stepwise_regression_od
import mplcursors  # Necesitarás instalar: pip install mplcursors

def grafico_temp_od_ph(observaciones, temperatura, od, ph):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

    # Gráfico de temperatura
    line1 = ax1.plot(observaciones, temperatura, 'o-', color="dodgerblue")
    ax1.set_xlabel("Observaciones")
    ax1.set_ylabel("Temperatura (°C)")
    ax1.set_title("Variaciones de temperatura del Río Atoyac ")
    ax1.set_ylim(0, 30)
    ax1.set_yticks(range(0, 31, 5))
    
    # Añadir cursor interactivo
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nTemp: {sel.target[1]:.2f}°C'))

    # Gráfico de OD y pH
    line2 = ax2.plot(observaciones, od, 'o-', label="OD (mg/L)", color="dodgerblue")
    line3 = ax2.plot(observaciones, ph, 'o-', label="pH", color="gray")
    ax2.set_xlabel("Observaciones")
    ax2.set_ylabel("Valor del parámetro")
    ax2.set_title("Valores de OD y pH en las muestras")
    ax2.legend()
    ax2.set_ylim(-1, 10)
    ax2.set_yticks(range(-1, 10, 1))
    
    # Añadir cursores interactivos
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nOD: {sel.target[1]:.2f} mg/L'))
    
    cursor3 = mplcursors.cursor(line3, hover=True)
    cursor3.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\npH: {sel.target[1]:.2f}'))

    plt.tight_layout()
    plt.show()

def grafico_od_ph(observaciones, od, ph):
    fig, ax = plt.subplots(figsize=(14, 8))

    line1 = ax.plot(observaciones, od, 'o-', label="OD (mg/L)", color="dodgerblue")
    line2 = ax.plot(observaciones, ph, 'o-', label="pH", color="gray")
    ax.set_xlabel("Observaciones")
    ax.set_ylabel("Valor del parámetro")
    ax.set_title("Valores de OD y pH del Río Atoyac, Puebla")
    ax.legend()
    ax.set_ylim(-1, 10)
    ax.set_yticks(range(-1, 10, 1))
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nOD: {sel.target[1]:.2f} mg/L'))
    
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\npH: {sel.target[1]:.2f}'))
    
    plt.tight_layout()
    plt.show()

def grafico_temp(observaciones, temperatura):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    line = ax.plot(observaciones, temperatura, 'o-', color="dodgerblue")
    ax.set_xlabel("Observaciones")
    ax.set_ylabel("Temperatura (°C)")
    ax.set_title("Variaciones de temperatura del Río Atoyac, Puebla")
    ax.set_ylim(0, 30)
    ax.set_yticks(range(0, 31, 5))
    
    # Cursor interactivo
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nTemp: {sel.target[1]:.2f}°C'))

    plt.tight_layout()
    plt.show()

def plot_sst(observaciones, sst):
    fig, ax = plt.subplots(figsize=(10, 6))
    line = ax.plot(observaciones, sst, 'o-', color='orange', label='TSS (mg/L)', markersize=5)
    ax.set_xlabel("Observaciones")
    ax.set_ylabel("Valor Parametro")
    ax.set_yscale("log")
    ax.set_title("SST 8 años")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    
    # Cursor interactivo
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nSST: {sel.target[1]:.2f} mg/L'))
    
    plt.show()

def plot_dqo(observaciones, dqo):
    fig, ax = plt.subplots(figsize=(10, 6))
    line = ax.plot(observaciones, dqo, 'd-', color='gray', label='DQO (mg/L)', markersize=5)
    ax.set_xlabel("Observaciones")
    ax.set_ylabel("Valor Parametro")
    ax.set_yscale("log")
    ax.set_title("COD 8 años")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    
    # Cursor interactivo
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nDQO: {sel.target[1]:.2f} mg/L'))
    
    plt.show()

def plot_dbo5(observaciones, dbo5):
    fig, ax = plt.subplots(figsize=(10, 6))
    line = ax.plot(observaciones, dbo5, 'o-', color='green', label='BOD5 (mg/L)', markersize=5)
    ax.set_xlabel("Observaciones")
    ax.set_ylabel("Valor Parametro")
    ax.set_yscale("log")
    ax.set_title("BOD5 8 años")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    
    # Cursor interactivo
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nBOD5: {sel.target[1]:.2f} mg/L'))
    
    plt.show()

def plot_dqo_sst_dbo5(observaciones, dqo, sst, dbo5):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_yscale('log')

    line1 = ax.plot(observaciones, dqo, 'd-', color='gray', label='COD (mg/L)', markersize=5)
    line2 = ax.plot(observaciones, sst, 'o-', color='orange', label='TSS (mg/L)', markersize=5)
    line3 = ax.plot(observaciones, dbo5, 'o-', color='yellow', label='BOD5 (mg/L)', markersize=5)

    ax.set_xlabel('Observaciones')
    ax.set_ylabel('Valor Parametro')
    ax.set_title('SST, COD, BOD5 8 años')
    ax.legend()
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nCOD: {sel.target[1]:.2f} mg/L'))
    
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nTSS: {sel.target[1]:.2f} mg/L'))
    
    cursor3 = mplcursors.cursor(line3, hover=True)
    cursor3.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nBOD5: {sel.target[1]:.2f} mg/L'))
    
    plt.show()

def plot_dbo5_vs_predicted(dbo5, y_pred):
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(dbo5, y_pred, color="purple", alpha=0.7, label="Valores Predichos")
    ax.plot([dbo5.min(), dbo5.max()], [dbo5.min(), dbo5.max()], 'k--', lw=2)
    ax.set_xlabel("DBO5 Medida")
    ax.set_ylabel("DBO5 Prevista")
    ax.set_title("DBO5 medida vs. valores predichos")
    
    # Cursor interactivo
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Medida: {sel.target[0]:.2f}\nPredicha: {sel.target[1]:.2f}'))
    
    print("Rango de DBO5 Medida:", dbo5.min(), "-", dbo5.max())
    print("Rango de DBO5 Predicha:", y_pred.min(), "-", y_pred.max())
    plt.show()

def plot_residuals(dbo5, y_pred):
    residuos = dbo5 - y_pred

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

    # Diferencia entre DBO5 medida y DBO5 predicha
    scatter1 = ax1.scatter(dbo5, dbo5 - y_pred, color="red", alpha=0.7)
    ax1.axhline(0, color='black', linestyle='--')
    ax1.set_xlabel("DBO5 Medida")
    ax1.set_ylabel("Diferencia (DBO5 Medida - DBO5 Predicha)")
    ax1.set_title("Diferencia entre DBO5 Medida y DBO5 Predicha")
    
    cursor1 = mplcursors.cursor(scatter1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'Medida: {sel.target[0]:.2f}\nDiferencia: {sel.target[1]:.2f}'))

    # Gráfico de residuos vs. valores predichos
    scatter2 = ax2.scatter(y_pred, residuos, color="green", alpha=0.7)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_xlabel("DBO5 Prevista")
    ax2.set_ylabel("Residuos")
    ax2.set_title("Gráfico de residuos vs. DBO5 predicha")
    
    cursor2 = mplcursors.cursor(scatter2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'Predicha: {sel.target[0]:.2f}\nResiduo: {sel.target[1]:.2f}'))

    plt.tight_layout()
    plt.show()

def graficar_bod5_vs_pred_medidos(BOD5_medidos, BOD5_predichos):
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(BOD5_medidos, BOD5_predichos, color='blue', label='Valores Medidos vs Predichos')
    ax.plot([min(BOD5_medidos), max(BOD5_medidos)], [min(BOD5_medidos), max(BOD5_medidos)], 'r--', label='Línea de Identidad')
    ax.set_title('Fitness of Measured BOD5 vs Predicted BOD5 for 333 Observations')
    ax.set_xlabel('Measured BOD5')
    ax.set_ylabel('Predicted BOD5')
    ax.legend()
    
    # Cursor interactivo
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Medido: {sel.target[0]:.2f}\nPredicho: {sel.target[1]:.2f}'))
    
    plt.show()

def plot_bod5_comparison(observations, measured, predicted):
    fig, ax = plt.subplots(figsize=(10, 6))

    line1 = ax.plot(observations, measured, color='blue', label='Valores Medidos', marker='o', linestyle='-', markersize=5)
    line2 = ax.plot(observations, predicted, color='red', label='Valores Predichos', marker='o', linestyle='-', markersize=5)

    ax.set_title('Comparación de Valores Medidos y Predichos de DBO5')
    ax.set_xlabel('Observaciones')
    ax.set_ylabel('DBO5')
    ax.legend()
    ax.grid(True)
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nMedido: {sel.target[1]:.2f}'))
    
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'Obs: {int(sel.target[0])}\nPredicho: {sel.target[1]:.2f}'))
    
    plt.show()

def graficar_prediccion_dqo(COD, BOD5_observado):
    model = LinearRegression()
    model.fit(COD.reshape(-1, 1), BOD5_observado)
    BOD5_predicho = model.predict(COD.reshape(-1, 1))
    COD_range = np.linspace(min(COD), max(COD), 500).reshape(-1, 1)
    BOD5_line = model.predict(COD_range)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter1 = ax.scatter(COD, BOD5_observado, color='blue', label='BOD5 Observado', alpha=0.7)
    scatter2 = ax.scatter(COD, BOD5_predicho, color='orange', label='BOD5 Predicho', alpha=0.7)
    ax.plot(COD_range, BOD5_line, color='black', label='Línea de Predicción (Regresión)', linewidth=2)
    
    ax.set_title('DQO vs BOD5 - Predicción Lineal', fontsize=14)
    ax.set_xlabel('DQO', fontsize=12)
    ax.set_ylabel('BOD5', fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(scatter1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'DQO: {sel.target[0]:.2f}\nBOD5 Obs: {sel.target[1]:.2f}'))
    
    cursor2 = mplcursors.cursor(scatter2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'DQO: {sel.target[0]:.2f}\nBOD5 Pred: {sel.target[1]:.2f}'))
    
    plt.tight_layout()
    plt.show()

def graficar_prediccion_od(OD, BOD5_observado):
    model = LinearRegression()
    model.fit(OD.reshape(-1, 1), BOD5_observado)
    BOD5_predicho = model.predict(OD.reshape(-1, 1))
    OD_range = np.linspace(min(OD), max(OD), 500).reshape(-1, 1)
    BOD5_line = model.predict(OD_range)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter1 = ax.scatter(OD, BOD5_observado, color='blue', label='BOD5 Observado', alpha=0.7)
    scatter2 = ax.scatter(OD, BOD5_predicho, color='orange', label='BOD5 Predicho', alpha=0.7)
    ax.plot(OD_range, BOD5_line, color='black', label='Línea de Predicción (Regresión)', linewidth=2)
    
    ax.set_title('SST vs BOD5 - Predicción Lineal', fontsize=14)
    ax.set_xlabel('SST', fontsize=12)
    ax.set_ylabel('BOD5', fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(scatter1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'SST: {sel.target[0]:.2f}\nBOD5 Obs: {sel.target[1]:.2f}'))
    
    cursor2 = mplcursors.cursor(scatter2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'SST: {sel.target[0]:.2f}\nBOD5 Pred: {sel.target[1]:.2f}'))
    
    plt.tight_layout()
    plt.show()

def plot_tss_bod5_relationship(cod, dbo5):
    model = stepwise_regression_od(cod, dbo5)
    BOD5_predichos = calcular_BOD5_OD(cod)
    
    fig, ax = plt.subplots(figsize=(10, 6))

    line1 = ax.plot(cod, dbo5, color='blue', label='Valores Medidos', marker='o', linestyle='-', markersize=5)
    line2 = ax.plot(cod, BOD5_predichos, color='red', label='Valores Predichos', marker='o', linestyle='-', markersize=5)

    ax.set_title('Comparación de Valores Medidos y Predichos de DBO5')
    ax.set_xlabel('Observaciones')
    ax.set_ylabel('DBO5')
    ax.legend()
    ax.grid(True)
    
    # Cursores interactivos
    cursor1 = mplcursors.cursor(line1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'COD: {sel.target[0]:.2f}\nMedido: {sel.target[1]:.2f}'))
    
    cursor2 = mplcursors.cursor(line2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(
        f'COD: {sel.target[0]:.2f}\nPredicho: {sel.target[1]:.2f}'))
    
    plt.show()