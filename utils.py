#!/usr/bin/python3

__name__ = "utils"
__author__= "Melissa Maureen Sales Brito"
__copyright__= "Equipo 9"
__version__= "1.0"
__credits__= "Materia EDO 2do CC"

import math
import plotly.graph_objects as plt
import sympy as sy
import pandas as pnd

def Convert_to_DF(points, tags):
    df_points = pnd.DataFrame(points, columns=tags)
    return df_points

def Combine_DataFrames(tags, dfs):
    combined_df = pnd.concat(dfs, axis=1, keys=tags)
    return combined_df

def Convert_to_Symbols(function_string):
    x, y = sy.symbols('x, y')
    function = sy.sympify(function_string)
    function = sy.lambdify([x,y], function, "numpy")
    return x, y, function

def Get_Trace(points, Name):
    x_values = [float(point[0]) for point in points]
    y_values = [float(point[1]) for point in points]
    figure = plt.Figure()
    trace = plt.Scatter(x=x_values, y=y_values, mode='lines+markers', name= Name)
    figure.add_trace(trace)
    figure.update_layout(
        title= Name,
        xaxis_title='X',
        yaxis_title='Y',
    )
    return (trace, figure)

def Get_Comparison_Traces(traces):
    data = []
    for trace in traces:
        data.append(trace)
    figure = plt.Figure(data=data)
    return figure

def Exact_Solution_R1(function_str, values):
    x = sy.symbols('x')
    function = sy.sympify(function_str)
    exact_solution = []
    for point in values:
        exact_solution.append((point, function.subs(x, point)))
    return exact_solution

def Get_Absolute_Error(exact_solution, numerical_solution):
    absolute_error = []
    for exact, numerical in zip(exact_solution, numerical_solution):
        error = math.fabs(exact - numerical)
        absolute_error.append(error)
    return absolute_error

def Get_Relative_Error(exact_solution, numerical_solution):
    relative_error = []
    for exact, numerical in zip(exact_solution, numerical_solution):
        if exact != 0:
            error = math.fabs((exact - numerical) / exact)
        else:
            error = float('inf')
        relative_error.append(error)
    return relative_error

