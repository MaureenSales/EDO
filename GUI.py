import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
import pandas as pd  # Ensure pandas is imported
from tkinter import messagebox
import ode_solver as solver
import utils as utils


#Solve Method
global values_dict
values_dict = {}
def solveEDO():
    try:
        funcValue = func.get()
        x0Value = float(x0.get())
        y0Value = float(y0.get())
        hValue = float(h.get())
        nValue = int(n.get())

        selectedMethods = [method for method, var in methodVars.items() if var.get()]

        if not selectedMethods:
            raise ValueError("Por favor, seleccione al menos un método")

        result_text = "Soluciones aproximadas:\n"
        for methods in selectedMethods:
            if methods == "Euler":
                print("Euler")
                values = solver.euler_method(funcValue, x0Value, y0Value, hValue, nValue)
            elif methods == "Euler Mejorado":
                print("Euler Mejorado")
                values = solver.euler_improved_method(funcValue, x0Value, y0Value, hValue, nValue)
            elif methods == "RK4":
                print("RK4")
                values = solver.RK4(funcValue, x0Value, y0Value, hValue, nValue)
            else:
                print("not method")
                values = None

            if values is not None:
                values_dict[methods] = values
                result_text += f"{methods}: y = {values[-1][1]:.4f} en x = {values[-1][0]}\n"
            else:
                result_text += f"{methods}: No se pudo calcular\n"

        resultValues.set(result_text)

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {str(e)}")

#Graph Comparison Method

def graphComparison():
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

root = tk.Tk()

#ttk styling configuration

style = ttk.Style()

style.configure('TLabel', 
                font=('Comic Sans MS', 12), 
                foreground='#ffffff',
                background='#2d3250')                               #label's style

style.configure('TCheckbutton', 
                font=('Comic Sans MS', 10), 
                foreground='#ffffff',
                background='#2d3250', 
                indicatorbackground = "sandy brown" )               #check buttons style

style.configure('TEntry', foreground='#ffffff', bg = '#424769')     #entry's style

root.title("Resolución de Ecuaciones Diferenciales")                #windows'title

root.geometry("1320x700")                                           #windows'size

root.iconbitmap("edoi.ico")                                         #windows'icon

root.resizable(True, True)                                        #disable window's resize

root.config(cursor="hand2", 
            bg = "#2d3250")                                         #window's design


#input frame

inputFrame = tk.Frame().place(x = 30, 
                        y = 30, 
                        width= 300)

#imput data

func = StringVar()
x0 = StringVar()
y0 = StringVar()
h = StringVar()
n = StringVar()


funcLabel = ttk.Label(inputFrame, text="Introduce los datos a continuacion:"). place(x = 30, y = 1)

#function y'
funcLabel = ttk.Label(inputFrame, 
                    text="y' =")
funcLabel.place(x=30, y=40)

functionInput = tk.Entry(inputFrame, 
                        textvariable=func, 
                        foreground='#ffffff', 
                        bg = '#424769', 
                        font=('Comic Sans MS', 12), 
                        border = 0)

functionInput.place(x = 70, 
                    y = 40, 
                    width= 300 - 70)


#value x0
x0Label = ttk.Label(inputFrame, text="x0 =")
x0Label.place(x=30, y=75)

x0Input = tk.Entry(inputFrame, 
                textvariable=x0, 
                foreground='#ffffff', 
                bg = '#424769', 
                font=('Comic Sans MS', 12), 
                border = 0)
x0Input.place(x = 70, y = 75, width= 300 - 70)


#value y0
y0Label = ttk.Label(inputFrame, text="y0 =")
y0Label.place(x=30, y=110)

y0Input = tk.Entry(inputFrame, 
                textvariable=y0, 
                foreground='#ffffff', 
                bg = '#424769', 
                font=('Comic Sans MS', 12), 
                border = 0)
y0Input.place(x = 70, y = 110, width= 300 - 70)



#value h
hLabel = ttk.Label(inputFrame, text="paso h =")
hLabel.place(x=30, y=145)

hInput = tk.Entry(inputFrame, 
                textvariable=h, 
                foreground='#ffffff', 
                bg = '#424769', 
                font=('Comic Sans MS', 12), 
                border = 0)
hInput.place(x = 96, y = 145, width= 300 - 96)



#value initial condition
initialCondLabel = ttk.Label(inputFrame, text="Número de pasos =")
initialCondLabel.place(x=30, y=180)

initialCondInput = tk.Entry(inputFrame, 
                            textvariable=n, 
                            foreground='#ffffff', 
                            bg = '#424769', 
                            font=('Comic Sans MS', 12), 
                            border = 0)
initialCondInput.place(x = 173, y = 180, width= 300 - 173)



# selectMenu

methodVars = {
    "Euler": tk.BooleanVar(),
    "Euler Mejorado": tk.BooleanVar(),
    "RK4": tk.BooleanVar()
}

ttk.Label(inputFrame, text="Selecciona los métodos:").place(x=30, y=215)
ttk.Checkbutton(inputFrame, text="Euler" , variable=methodVars["Euler"]).place(x=60, y=250)
ttk.Checkbutton(inputFrame, text="Euler Mejorado", variable=methodVars["Euler Mejorado"]).place(x=60, y=285)
ttk.Checkbutton(inputFrame, text="RK4", variable=methodVars["RK4"]).place(x=60, y=320)

#solve button
solveButton = tk.Button(inputFrame, 
                        text= "Resolver", 
                        font=('Comic Sans MS', 12), 
                        width= 26, 
                        foreground='#2d3250', 
                        bg = "sandy brown", 
                        border=0, 
                        command= solveEDO
                        )
solveButton.place(x = 30, y = 355)

#Comparison button
comparisonButton = tk.Button(inputFrame, 
                        text= "Comparar graficos", 
                        font=('Comic Sans MS', 12), 
                        width= 26, 
                        foreground='#2d3250', 
                        bg = "sandy brown", 
                        border=0,
                        command=graphComparison )
comparisonButton.place(x = 30, y = 400)

#DataFrame button
dataframeButton = tk.Button(inputFrame, 
                        text= "Convertir a DataFrame", 
                        font=('Comic Sans MS', 12), 
                        width= 26, 
                        foreground='#2d3250', 
                        bg = "sandy brown", 
                        border=0,
                        )
dataframeButton.place(x = 30, y = 445)

#numericErrors
numericErrors = tk.Button(inputFrame, 
                        text="Errores Númericos", 
                        font=('Comic Sans MS', 12), 
                        width= 26, 
                        foreground='#2d3250', 
                        bg = "sandy brown", 
                        border=0,
                        )
numericErrors.place(x = 30, y = 490)

#Isoclines
isoclinesButton = tk.Button(inputFrame, 
                        text="Graficar campo direccional", 
                        font=('Comic Sans MS', 12), 
                        width= 26, 
                        foreground='#2d3250', 
                        bg = "sandy brown", 
                        border=0 )
isoclinesButton.place(x = 30, y = 535)



#output frame

outputFrame = tk.Frame().place(x = 400, 
                        y = 30, 
                        width= 1000)

#result
resultLabel = ttk.Label(outputFrame, text="Resultado:")
resultLabel.place(x=400, y=40)

resultValues = tk.StringVar()
ttk.Label(root, textvariable=resultValues).place(x=400, y=75)

root.mainloop()