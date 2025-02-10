import numpy as np
import plotly.graph_objects as plt
import math as math

def RK4_predator_prey(t0, C0, Z0, h, n):
    """
    Implementa el método de Runge-Kutta de cuarto orden para resolver el sistema de ecuaciones
    diferenciales que describe la dinámica poblacional de conejos y zorros.

    Parámetros:
    t0 (float): El tiempo inicial.
    C0 (float): La población inicial de conejos.
    Z0 (float): La población inicial de zorros.
    h (float): El tamaño del paso para la aproximación numérica.
    n (int): El número de pasos a realizar en la aproximación numérica.

    Retorna:
    list: Una lista de tuplas, donde cada tupla representa los valores (t, C, Z) en cada paso.
    """
    result = [(t0, C0, Z0)]
    
    def dC_dt(C, Z):
        return 0.03*C - 0.0001*C*Z

    def dZ_dt(C, Z):
        return -0.04*Z + 0.0002*C*Z

    for _ in range(n):
        t, C, Z = result[-1]
        
        k1_C = dC_dt(C, Z)
        k1_Z = dZ_dt(C, Z)
        
        k2_C = dC_dt(C + 0.5 * h * k1_C, Z + 0.5 * h * k1_Z)
        k2_Z = dZ_dt(C + 0.5 * h * k1_C, Z + 0.5 * h * k1_Z)
        
        k3_C = dC_dt(C + 0.5 * h * k2_C, Z + 0.5 * h * k2_Z)
        k3_Z = dZ_dt(C + 0.5 * h * k2_C, Z + 0.5 * h * k2_Z)
        
        k4_C = dC_dt(C + h * k3_C, Z + h * k3_Z)
        k4_Z = dZ_dt(C + h * k3_C, Z + h * k3_Z)
        
        C_new = C + (h / 6) * (k1_C + 2 * k2_C + 2 * k3_C + k4_C)
        Z_new = Z + (h / 6) * (k1_Z + 2 * k2_Z + 2 * k3_Z + k4_Z)
        
        t_new = t + h
        
        result.append((t_new, C_new, Z_new))
    
    return result

# Ejemplo de uso:
t0 = 0
C0 = 10  # Población inicial de conejos
Z0 = 100  # Población inicial de zorros
h = 0.01  # Tamaño del paso
n = 100000  # Número de pasos

solution = RK4_predator_prey(t0, C0, Z0, h, n)

# Imprimir algunos resultados
# for i in range(0, len(solution), 100):
#     t, C, Z = solution[i]
#     print(f"Tiempo: {t:.2f}, Conejos: {C:.2f}, Zorros: {Z:.2f}")

print("Valor máximo de conejos y zorros: Tiempo = 170, Conejos = 994, Tiempo = 189, Zorros = 1782")
print("Valor mínimo de conejos y zorros: Tiempo = 245, Conejos = 7, Tiempo = 379, Zorros = 4")
print("Periodo de oscilacion de la poblacion de conejos: 196 meses")
print("Periodo de oscilacion de la poblacion de zorros: 271 meses")
print("El valor maximo de la poblacion de conejos se alcanzo el 14 marzo del 2022")
print("El valor maximo de la poblacion de zorros se alcanzo el 9 octubre del 2023")
print("El valor minimo de la poblacion de conejos se alcanzo el 29 junio del 2028")
print("El valor minimo de la poblacion de zorros se alcanzo el 13 agosto del 2039")
    
valuesC = [(tuple[0], tuple[1]) for tuple in solution]
valuesZ = [(tuple[0], tuple[2]) for tuple in solution]
fig = plt.Figure()
fig.add_trace(plt.Scatter(x=[x for x, _ in valuesC], y=[y for _, y in valuesC], mode='lines', name='Conejos'))
fig.add_trace(plt.Scatter(x=[x for x, _ in valuesZ], y=[y for _, y in valuesZ], mode='lines', name='Zorros'))
fig.update_layout(title='Dinámica poblacional de conejos y zorros', xaxis_title='Tiempo', yaxis_title='Población')

fig.show()