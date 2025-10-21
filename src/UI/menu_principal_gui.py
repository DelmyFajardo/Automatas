import tkinter as tk
from tkinter import messagebox

class MenuPrincipalGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto - Autómatas y Lenguajes Formales")
        self.geometry("480x240")
        self.resizable(False, False)

        header = tk.Label(self, text="PROYECTO FINAL - AUTÓMATAS Y LENGUAJES FORMALES", font=("Segoe UI", 12, "bold"))
        header.pack(pady=(18, 8))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        btn_buscar = tk.Button(btn_frame, text=" Buscador de patrones", width=30, command=self.abrir_busqueda)
        btn_buscar.grid(row=0, column=0, padx=8, pady=6)

        btn_generar = tk.Button(btn_frame, text=" Generador de palabras", width=30, command=self.abrir_generador)
        btn_generar.grid(row=1, column=0, padx=8, pady=6)

        btn_salir = tk.Button(self, text="Salir", width=20, command=self.quit)
        btn_salir.pack(pady=(12, 6))

    def abrir_busqueda(self):
        messagebox.showinfo("Buscador", "Entrando al módulo de búsqueda de patrones (pendiente de implementar)")

    def abrir_generador(self):
        messagebox.showinfo("Generador", "Entrando al módulo de generación de palabras (pendiente de implementar)")


def main():
    app = MenuPrincipalGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
