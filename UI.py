import pandas as pd  # Ensure pandas is imported
import tkinter as tk
from tkinter import ttk, messagebox
import ode_solver as solver
import utils as utils

# Función para resolver la ecuación diferencial usando el método seleccionado
global values_dict
values_dict = {}
def resolver():
    try:
        function = entry_function.get()
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        h = float(entry_h.get())
        n = int(entry_n.get())

        metodos_seleccionados = [metodo for metodo, var in metodo_vars.items() if var.get()]

        if not metodos_seleccionados:
            raise ValueError("Por favor, seleccione al menos un método")

        resultado_text = "Soluciones aproximadas:\n"
        for metodo in metodos_seleccionados:
            if metodo == "Euler":
                values = solver.euler_method(function, x0, y0, h, n)
            elif metodo == "Euler Mejorado":
                values = solver.euler_improved_method(function, x0, y0, h, n)
            elif metodo == "RK4":
                values = solver.RK4(function, x0, y0, h, n)
            else:
                values = None

            if values is not None:
                values_dict[metodo] = values
                resultado_text += f"{metodo}: y = {values[-1][1]:.4f} en x = {values[-1][0]}\n"
            else:
                resultado_text += f"{metodo}: No se pudo calcular\n"

        resultado_var.set(resultado_text)

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {str(e)}")

# Función para graficar las trazas de las aproximaciones
def graficar_comparacion():
    try:
        if not values_dict:
            raise ValueError("Primero debe resolver la ecuación")
        
        traces = []
        for metodo, values in values_dict.items():
            trace, _ = utils.Get_Trace(values, metodo)
            traces.append(trace)
        
        figure = utils.Get_Comparison_Traces(traces)
        figure.show()  # Mostrar la gráfica comparativa
    except Exception as e:
        # Mostrar un mensaje de error si ocurre una excepción al graficar
        messagebox.showerror("Error", f"Hubo un error al graficar la comparación: {str(e)}")

# Función para calcular los errores absoluto y relativo
def calcular_errores():
    try:
        resolver()  # Arreglar metodo (calculo de sol ext)
        for metodo, values in values_dict.items():
            exact_solution = utils.Exact_Solution_R1(entry_function.get(), values)
            abs_error = utils.Get_Absolute_Error(exact_solution, values)
            rel_error = utils.Get_Relative_Error(exact_solution, values)
            messagebox.showinfo(f"Errores - {metodo}", f"Error Absoluto: {abs_error}\nError Relativo: {rel_error}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al calcular los errores: {str(e)}")


# Función para convertir los resultados a un DataFrame de pandas
def convertir_a_dataframe():
    try:
        if not values_dict:
            raise ValueError("Primero debe resolver la ecuación")

        dfs = []
        for metodos, values in values_dict.items():
            df = utils.Convert_to_DF(values, ["x", "y"])
            dfs.append(df)
        if len(dfs) > 1:
            df = utils.Combine_DataFrames(metodos, dfs)
        mostrar_dataframe(df)  # Mostrar el DataFrame en una nueva ventana
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al convertir a DataFrame: {str(e)}")


# Función para mostrar el DataFrame en una nueva ventana
def mostrar_dataframe(df):
    #problemas con los data frames combinados
    # Crear una nueva ventana para mostrar el DataFrame
    df_window = tk.Toplevel(root)
    df_window.title("DataFrame")

    # Crear un Treeview para mostrar el DataFrame
    tree = ttk.Treeview(df_window, columns=list(df.columns), show='headings')
    tree.pack(expand=True, fill='both')
    
    for col in df.columns:
        print(col)
    # Configurar las columnas
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # Insertar los datos del DataFrame en el Treeview
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))





# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Resolución de EDO por Múltiples Métodos")
root.geometry("600x600")
root.resizable(True, True)

# Estilo
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10), padding=6)
style.configure("TRadiobutton", font=("Helvetica", 10))

# Etiquetas y campos de entrada
ttk.Label(root, text="Función (y' = f(x, y)):").grid(row=0, column=0, sticky="ew", padx=10, pady=5)
entry_function = ttk.Entry(root)
entry_function.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

ttk.Label(root, text="Valor inicial x0:").grid(row=1, column=0, sticky="ew", padx=10, pady=5)
entry_x0 = ttk.Entry(root)
entry_x0.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

ttk.Label(root, text="Valor inicial y0:").grid(row=2, column=0, sticky="ew", padx=10, pady=5)
entry_y0 = ttk.Entry(root)
entry_y0.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

ttk.Label(root, text="Paso (h):").grid(row=3, column=0, sticky="ew", padx=10, pady=5)
entry_h = ttk.Entry(root)
entry_h.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

ttk.Label(root, text="Cantidad de pasos:").grid(row=4, column=0, sticky="ew", padx=10, pady=5)
entry_n = ttk.Entry(root)
entry_n.grid(row=4, column=1, sticky="ew", padx=10, pady=5)

# Opciones para seleccionar el método
metodo_vars = {
    "Euler": tk.BooleanVar(),
    "Euler Mejorado": tk.BooleanVar(),
    "RK4": tk.BooleanVar()
}
ttk.Label(root, text="Selecciona los métodos:").grid(row=5, column=0, sticky="ew", padx=10, pady=5)
ttk.Checkbutton(root, text="Euler", variable=metodo_vars["Euler"]).grid(row=5, column=1, sticky="w", padx=10, pady=5)
ttk.Checkbutton(root, text="Euler Mejorado", variable=metodo_vars["Euler Mejorado"]).grid(row=6, column=1, sticky="w", padx=10, pady=5)
ttk.Checkbutton(root, text="RK4", variable=metodo_vars["RK4"]).grid(row=7, column=1, sticky="w", padx=10, pady=5)

# Etiqueta para mostrar el resultado
resultado_var = tk.StringVar()
ttk.Label(root, textvariable=resultado_var, wraplength=500).grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
# Botones
boton_resolver = ttk.Button(root, text="Resolver", command=resolver)
boton_resolver.grid(row=9, column=0, sticky="ew", padx=10, pady=10)

boton_graficar_comparacion = ttk.Button(root, text="Graficar Comparación", command=graficar_comparacion)
boton_graficar_comparacion.grid(row=9, column=1, sticky="ew", padx=10, pady=10)

boton_errores = ttk.Button(root, text="Calcular Errores", command=calcular_errores)
boton_errores.grid(row=10, column=0, sticky="ew", padx=10, pady=10)

boton_dataframe = ttk.Button(root, text="Convertir a DataFrame", command=convertir_a_dataframe)
boton_dataframe.grid(row=10, column=1, sticky="ew", padx=10, pady=10)

# Configurar las columnas para que se expandan
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Iniciar la ventana
root.mainloop()

