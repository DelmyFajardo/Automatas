
import re
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from manejo_gramaticas import GRAMATICAS_PREDEFINIDAS, seleccionar_gramatica
import palabras_generadas_db
import motor_generacion

class InterfazGramaticas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Gramáticas - Proyecto Autómatas")
        self.geometry("470x420")
        self.configure(bg="#d7ccc8")  
        self.gramaticas_actuales = GRAMATICAS_PREDEFINIDAS.copy()
        palabras_generadas_db.crear_tablas()
        self.crear_widgets()

    def crear_widgets(self):
        header = tk.Label(self, text="Gestor de Gramáticas", font=("Segoe UI", 16, "bold"), fg="#4e342e", bg="#d7ccc8")
        header.pack(pady=(18, 8))

        sub = tk.Label(self, text="Seleccione una gramática:", font=("Segoe UI", 11), bg="#d7ccc8", fg="#37474f")
        sub.pack(pady=(0, 10))

        frame_lista = tk.Frame(self, bg="#d7ccc8")
        frame_lista.pack(pady=(0, 10))
        self.lista_gramaticas = tk.Listbox(frame_lista, font=("Segoe UI", 12), height=7, width=28, bd=2, relief="groove", fg="#222", bg="#fafafa", selectbackground="#bdbdbd", selectforeground="#222", selectmode=tk.SINGLE)
        self.actualizar_lista_gramaticas()
        self.lista_gramaticas.pack(side=tk.LEFT, padx=(0, 8))

        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_gramaticas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_gramaticas.config(yscrollcommand=scrollbar.set)

        frame_botones = tk.Frame(self, bg="#d7ccc8")
        frame_botones.pack(pady=(0, 10))

        self.btn_ver = tk.Button(frame_botones, text="Ver palabras almacenadas", command=self.ver_palabras, width=22, font=("Segoe UI", 11, "bold"), bg="#c8e6c9", fg="#263238", activebackground="#b3e5fc", activeforeground="#263238", relief="raised", bd=2)
        self.btn_ver.grid(row=0, column=1, padx=10, pady=8)

        self.btn_multi = tk.Button(frame_botones, text="Generar múltiples", command=self.generar_multiples, width=22, font=("Segoe UI", 10, "bold"), bg="#8fc3d9", fg="#263238", activebackground="#b3e5fc", activeforeground="#263238", relief="raised", bd=2)
        self.btn_multi.grid(row=1, column=0, columnspan=2, pady=(6, 0))

        btn_salir = tk.Button(self, text="Salir", command=self.destroy, width=12, font=("Segoe UI", 11, "bold"), bg="#4e342e", fg="white", activebackground="#a1887f", activeforeground="white", relief="raised", bd=2)
        btn_salir.pack(pady=(8, 0))

    def actualizar_lista_gramaticas(self):
        self.lista_gramaticas.delete(0, tk.END)
        for nombre in self.gramaticas_actuales:
            self.lista_gramaticas.insert(tk.END, nombre)

    def ver_palabras(self):
        seleccion = self.lista_gramaticas.curselection()
        if not seleccion:
            messagebox.showinfo("Info", "Seleccione una gramática.")
            return
        nombre = self.lista_gramaticas.get(seleccion)
        if nombre in GRAMATICAS_PREDEFINIDAS:
            if nombre == "contraseña":
                palabras = palabras_generadas_db.obtener_generico('contrasenas', limit=100)
            elif nombre == "correo":
                palabras = palabras_generadas_db.obtener_generico('correos', limit=100)
            elif nombre == "direccion":
                palabras = palabras_generadas_db.obtener_generico('direcciones', limit=100)
            elif nombre == "telefono":
                palabras = palabras_generadas_db.obtener_generico('telefonos', limit=100)
            elif nombre == "usuario":
                palabras = palabras_generadas_db.obtener_generico('usuarios', limit=100)
            else:
                palabras = []
        else:
            palabras = palabras_generadas_db.obtener_generico(nombre)

        top = tk.Toplevel(self)
        top.title(f"Palabras de '{nombre}'")
        top.geometry("400x300")
        top.configure(bg="#f5f5f5")
        label = tk.Label(top, text=f"Palabras de '{nombre}'", font=("Segoe UI", 12, "bold"), bg="#f5f5f5")
        label.pack(pady=(10, 5))
        listbox = tk.Listbox(top, font=("Segoe UI", 11), width=45, height=12, bg="#fff", fg="#222")
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(listbox, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        if palabras:
            for palabra in palabras:
                listbox.insert(tk.END, palabra)
        else:
            listbox.insert(tk.END, "No hay palabras almacenadas.")
        btn_cerrar = tk.Button(top, text="Cerrar", command=top.destroy)
        btn_cerrar.pack(pady=(0, 10))

    def generar_multiples(self):
        seleccion = self.lista_gramaticas.curselection()
        if not seleccion:
            messagebox.showinfo("Info", "Seleccione una gramática antes de generar.")
            return
        nombre = self.lista_gramaticas.get(seleccion)

        try:
            cantidad = simpledialog.askinteger("Generar múltiples", f"¿Cuántas '{nombre}' generar?", minvalue=1, initialvalue=1)
        except Exception:
            messagebox.showerror("Error", "Entrada inválida")
            return
        if not cantidad or cantidad <= 0:
            messagebox.showinfo("Generación", "Cantidad no válida o cancelada.")
            return

        extra = {}
        if nombre == 'usuario':
            min_len = simpledialog.askinteger("Usuarios", "Longitud mínima de usuario:", minvalue=1, initialvalue=3)
            if min_len is None:
                return
            max_len = simpledialog.askinteger("Usuarios", "Longitud máxima de usuario:", minvalue=1, initialvalue=12)
            if max_len is None or min_len > max_len:
                messagebox.showerror("Error", "Longitudes inválidas")
                return
            extra['min_len'] = min_len
            extra['max_len'] = max_len
        elif nombre == 'contraseña':
            length = simpledialog.askinteger("Contraseñas", "Longitud de las contraseñas:", minvalue=6, initialvalue=12)
            if length is None or length < 1:
                messagebox.showerror("Error", "Longitud inválida")
                return
            extra['length'] = length


        def worker(extra):
            try:
                count = 0
                if nombre == 'usuario':
                    generadas = motor_generacion.generar_usuarios_personalizados(cantidad, min_len=extra.get('min_len'), max_len=extra.get('max_len'))
                elif nombre == 'contraseña':
                    generadas = motor_generacion.generar_contrasenas_seguras(cantidad, length=extra.get('length'))
                else:
                    max_tokens_map = {
                        'correo': 25,
                        'direccion': 30,
                        'telefono': 15
                    }
                    generadas = motor_generacion.generar_varias(nombre, cantidad, max_tokens=max_tokens_map.get(nombre, 20))

                try:
                    if nombre == 'contraseña' and hasattr(palabras_generadas_db, 'insertar_contrasenas_batch'):
                        palabras_generadas_db.insertar_contrasenas_batch(generadas)
                        count = len(generadas)
                    elif nombre == 'correo' and hasattr(palabras_generadas_db, 'insertar_correos_batch'):
                        palabras_generadas_db.insertar_correos_batch(generadas)
                        count = len(generadas)
                    elif nombre == 'direccion' and hasattr(palabras_generadas_db, 'insertar_direcciones_batch'):
                        palabras_generadas_db.insertar_direcciones_batch(generadas)
                        count = len(generadas)
                    elif nombre == 'telefono' and hasattr(palabras_generadas_db, 'insertar_telefonos_batch'):
                        palabras_generadas_db.insertar_telefonos_batch(generadas)
                        count = len(generadas)
                    elif nombre == 'usuario' and hasattr(palabras_generadas_db, 'insertar_usuarios_batch'):
                        palabras_generadas_db.insertar_usuarios_batch(generadas)
                        count = len(generadas)
                    else:
                        for g in generadas:
                            if nombre == 'contraseña':
                                palabras_generadas_db.insertar_contrasena(g)
                            elif nombre == 'correo':
                                palabras_generadas_db.insertar_correo(g)
                            elif nombre == 'direccion':
                                palabras_generadas_db.insertar_direccion(g)
                            elif nombre == 'telefono':
                                palabras_generadas_db.insertar_telefono(g)
                            elif nombre == 'usuario':
                                palabras_generadas_db.insertar_usuario(g)
                            count += 1
                except Exception as e:
                    for g in generadas:
                        try:
                            if nombre == 'contraseña':
                                palabras_generadas_db.insertar_contrasena(g)
                            elif nombre == 'correo':
                                palabras_generadas_db.insertar_correo(g)
                            elif nombre == 'direccion':
                                palabras_generadas_db.insertar_direccion(g)
                            elif nombre == 'telefono':
                                palabras_generadas_db.insertar_telefono(g)
                            elif nombre == 'usuario':
                                palabras_generadas_db.insertar_usuario(g)
                            count += 1
                        except Exception:
                            continue

                self.after(0, lambda: messagebox.showinfo("Generación completada", f"Se generaron y almacenaron {count} elementos para '{nombre}'."))
            except Exception as e:
                self.after(0, lambda exc=e: messagebox.showerror("Error", f"Error durante la generación: {exc}"))
            finally:
                try:
                    self.after(0, lambda: self.btn_multi.config(state=tk.NORMAL))
                    self.after(0, lambda: self.btn_ver.config(state=tk.NORMAL))
                except Exception:
                    pass

        threading.Thread(target=worker, args=(extra,), daemon=True).start()

if __name__ == "__main__":
    palabras_generadas_db.crear_tablas()
    app = InterfazGramaticas()
    app.mainloop()
