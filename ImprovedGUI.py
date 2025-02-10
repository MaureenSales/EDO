from customtkinter import *

root = CTk()
root.title("Resolución de Ecuaciones Diferenciales")                
root.geometry("1320x700")                                          
root.iconbitmap("edoi.ico")                                        
root.resizable(True, True)                                        
root.config(cursor="hand2", 
            bg = "#2d3250")

set_appearance_mode("dark")

btn = CTkButton(master=root, text = "clickme", corner_radius= 10,  fg_color= "sandy brown", hover_color= '#424769', border_color= "sandy brown")
btn.place(x = 30, y = 30)

root.mainloop()