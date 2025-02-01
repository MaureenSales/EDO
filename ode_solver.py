import numpy as np
import sympy as sp
#!/usr/bin/python3

__name__ = "ode_solver"
__copyright__= "Equipo 9"
__version__= "1.0"
__credits__= "Materia EDO 2do CC"

import utils as utils
import sympy as sy


def euler_method(function_str, x_0, y_0, h, n):
    """
    Esta función implementa el Método de Euler para resolver ecuaciones diferenciales ordinarias (EDOs).

    Parámetros:
    function_str (str): Una representación en cadena de la función de la EDO en la forma dy/dx = f(x, y).
    x_0 (float): El valor inicial de la variable independiente x.
    y_0 (float): El valor inicial de la variable dependiente y.
    h (float): El tamaño del paso para la aproximación numérica.
    n (int): El número de pasos a realizar en la aproximación numérica.

    Retorna:
    list: Una lista de tuplas, donde cada tupla representa los valores (x, y) en cada paso.
    """
    _, _, function = utils.Convert_to_Symbols(function_str)
    result = [(x_0, y_0)]
    for _ in range(n):
        An = function(x_0,y_0)
        x_0 += h
        y_0 += h * An
        result.append((x_0, y_0))
    return result

def euler_improved_method(function_str, x_0, y_0, h, n):
    """
    Implementa el Método de Euler Mejorado (Método de Heun) para resolver ecuaciones diferenciales ordinarias (EDOs).

    Parámetros:
    function_str (str): Una representación en cadena de la función de la EDO en la forma dy/dx = f(x, y).
    x_0 (float): El valor inicial de la variable independiente x.
    y_0 (float): El valor inicial de la variable dependiente y.
    h (float): El tamaño del paso para la aproximación numérica.
    n (int): El número de pasos a realizar en la aproximación numérica.

    Retorna:
    list: Una lista de tuplas, donde cada tupla representa los valores (x, y) en cada paso.
    """

    x, y, function = utils.Convert_to_Symbols(function_str)
    result = [(x_0, y_0)]
    for _ in range(n):
        An_0 = function(x_0, y_0)
        x_0 += h
        y_1 = y_0 + h * An_0
        An_1 = (An_0 + function(x_0, y_1)) / 2
        y_0 += h * An_1
        result.append((x_0, y_0))
        return result


def RK4(function_str, x_0, y_0, h, n):
    """
    Implementa el método de Runge-Kutta de cuarto orden para resolver ecuaciones diferenciales ordinarias (EDOs).

    Parámetros:
    function_str (str): Una representación en cadena de la función de la EDO en la forma dy/dx = f(x, y).
    x_0 (float): El valor inicial de la variable independiente x.
    y_0 (float): El valor inicial de la variable dependiente y.
    h (float): El tamaño del paso para la aproximación numérica.
    n (int): El número de pasos a realizar en la aproximación numérica.

    Retorna:
    list: Una lista de tuplas, donde cada tupla representa los valores (x, y) en cada paso.
    """
    x, y, function = utils.Convert_to_Symbols(function_str)
    result = [(x_0, y_0)]
    for _ in range(n):
        k1 = function(x_0, y_0)
        k2 = function(x_0 + h/2, y_0 + (h/2)*k1)
        k3 = function(x_0 + h/2, y_0 + (h/2)*k2)
        k4 = function(x_0 + h, y_0 + h*k3)
        x_0 += h
        y_0 += (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        result.append((x_0, y_0))
    return result

