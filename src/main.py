import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
import os

# ⚠️ NOTA IMPORTANTE:
# Asegúrate de que tus importaciones internas funcionen. Si ejecutas 'py src/main.py', 
# puede que necesites usar el formato corregido:
try:
    from Expresiones_Regulares.Expresion import ExpresionSearcher
    # Placeholder para la funcionalidad de Gramáticas (Tarea 07/10 y 08/10)
    from Gramaticas.generator import GrammarGenerator, GRAMATICA_CONTRASENA , GRAMATICA_EMAIL, GRAMATICA_IPV4, GRAMATICA_DIRECCION, GRAMATICA_TELEFONO, GRAMATICA_USUARIO
except ImportError as e:
    # Intenta la importación de módulo si se ejecuta con 'py -m src.main'
    try:
        from src.Expresiones_Regulares.Expresion import ExpresionSearcher
        from src.Gramaticas.generator import GrammarGenerator, GRAMATICA_CONTRASENA, GRAMATICA_EMAIL, GRAMATICA_IPV4, GRAMATICA_DIRECCION, GRAMATICA_TELEFONO, GRAMATICA_USUARIO
    except ImportError as e_alt:
        print(f"ERROR DE MODULARIDAD: No se puede encontrar los módulos internos. {e_alt}")
        sys.exit(1)


class AutomaApp(tk.Tk):
    """Aplicación principal que contiene la GUI."""
    def __init__(self):
        super().__init__()
        self.title("PROYECTO AUTÓMATAS Y LENGUAJES FORMALES")
        self.geometry("800x600")
        
        # Contenedor principal para cambiar de vista (Regex o Gramáticas)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.current_frame = None
        self.create_main_menu()

    def create_main_menu(self):
        """Crea la interfaz inicial con botones para seleccionar el módulo."""
        # Limpia cualquier vista anterior
        if self.current_frame:
            self.current_frame.destroy()

        menu_frame = ttk.Frame(self.container)
        menu_frame.pack(expand=True)
        self.current_frame = menu_frame
        
        ttk.Label(menu_frame, text="PROYECTO AUTÓMATAS", font=("Arial", 18, "bold")).pack(pady=20)
        
        ttk.Button(menu_frame, text="1. Búsqueda de Patrones (Regex)", 
                   command=lambda: self.show_frame(RegexSearchFrame)).pack(pady=10, ipadx=50)
        
        ttk.Button(menu_frame, text="2. Generación de Palabras (Gramáticas)", 
                   command=lambda: self.show_frame(GrammarGenerationFrame)).pack(pady=10, ipadx=50)
        
        ttk.Button(menu_frame, text="3. Salir", 
                   command=self.destroy).pack(pady=20, ipadx=50)

    def show_frame(self, new_frame_class):
        """Muestra una nueva vista (Frame) y oculta la actual."""
        if self.current_frame:
            self.current_frame.destroy()
        
        # Instancia el nuevo Frame, pasándole la referencia a la aplicación
        new_frame = new_frame_class(self.container, self)
        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame


class RegexSearchFrame(ttk.Frame):
    """Interfaz Gráfica para la Búsqueda de Patrones (Regex)."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Variables de control ---
        self.regex_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.source_var.set("Ingreso Manual") # Valor por defecto

        # --- Interfaz de Entrada ---
        input_frame = ttk.LabelFrame(self, text="Entrada de Datos y Expresión Regular")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Fila 1: Regex
        ttk.Label(input_frame, text="Expresión Regular:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.regex_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Fila 2: Fuente
        ttk.Label(input_frame, text="Fuente del Texto:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Entrada de Fuente (para archivo o URL)
        self.source_entry = ttk.Entry(input_frame, textvariable=self.source_var, width=50)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.source_entry.bind("<FocusIn>", lambda event: self.source_entry.delete(0, "end") if self.source_var.get() == "Ingreso Manual" else None)
        
        # Botón para Archivo
        ttk.Button(input_frame, text="Abrir Archivo", command=self.open_file_dialog).grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Fila 3: Entrada Manual (Área de texto grande)
        manual_frame = ttk.LabelFrame(self, text="Texto para Ingreso Manual")
        manual_frame.pack(fill="x", padx=10, pady=5)
        self.manual_text = scrolledtext.ScrolledText(manual_frame, wrap=tk.WORD, height=8)
        self.manual_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Botón de Ejecución ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(btn_frame, text="BUSCAR PATRONES (Ejecutar)", command=self.execute_search).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="<- Volver al Menú Principal", command=controller.create_main_menu).pack(side="right", padx=5)


        # --- Interfaz de Salida ---
        output_frame = ttk.LabelFrame(self, text="Resultados de la Búsqueda (Línea, Columna, Coincidencia)")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

    def open_file_dialog(self):
        """Abre un diálogo para seleccionar un archivo local."""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.source_var.set(file_path)
            self.manual_text.delete("1.0", tk.END) # Limpia el área manual

    def execute_search(self):
        """Maneja la lógica de la Tarea 06/10: Ejecutar la búsqueda de patrones."""
        self.output_text.delete("1.0", tk.END)
        regex = self.regex_var.get().strip()
        source_id = self.source_var.get().strip()

        if not regex:
            messagebox.showerror("Error de Entrada", "Debe ingresar una Expresión Regular.")
            return

        # 1. Determinar la fuente del texto y cargarlo
        source_text = None
        
        if source_id == "Ingreso Manual" or not source_id:
            # Fuente 1: Entrada Manual (Tarea 05/10)
            source_text = self.manual_text.get("1.0", tk.END).strip()
            if not source_text:
                messagebox.showwarning("Advertencia", "No hay texto en el área manual.")
                return
        else:
            # Fuente 2/3: Archivo o URL (Tareas 05/10 y 07/10)
            searcher = ExpresionSearcher(regex)
            
            # load_text devolverá el texto si es exitoso
            if not searcher.load_text(source_id):
                # load_text ya imprime los errores (Archivo no encontrado, URL inválida)
                self.output_text.insert(tk.END, "ERROR al cargar la fuente. Revise la consola.\n")
                return
            
            # Si se carga desde archivo/URL, el texto está en el objeto searcher
            # Para esta GUI, cargaremos el texto en el área manual para mostrarlo
            self.manual_text.delete("1.0", tk.END)
            self.manual_text.insert(tk.END, searcher.text_content)
            source_text = searcher.text_content

        # 2. Ejecutar la búsqueda con la lógica de ExpresionSearcher
        searcher = ExpresionSearcher(regex)
        searcher.text_content = source_text # Asignamos el texto cargado

        results = searcher.execute_search() 
        
        # 3. Mostrar resultados
        if results:
            self.output_text.insert(tk.END, f"Se encontraron {len(results)} coincidencias:\n")
            for res in results:
                line = f"Línea {res['line_num']:<4} Col {res['col_start']:<4}: '{res['match']}'\n"
                self.output_text.insert(tk.END, line)
        else:
            self.output_text.insert(tk.END, "No se encontraron coincidencias.\n")


class GrammarGenerationFrame(ttk.Frame):
    """Interfaz Gráfica para la Generación de Palabras a partir de Gramáticas."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Definición de las 5 Gramáticas (Tarea 06/10)
        self.grammars = {
            "Contraseña Básica": GRAMATICA_CONTRASENA,
            "Correo Electrónico": GRAMATICA_EMAIL, 
            "Dirección IP": GRAMATICA_IPV4,
            "Dirección Física": GRAMATICA_DIRECCION,
            "Número de Teléfono": GRAMATICA_TELEFONO,
            "Nombre de Usuario": GRAMATICA_USUARIO
            # ... añadir las otras 2 gramáticas
        }
        
        # --- Variables de control ---
        self.selected_grammar = tk.StringVar(value="Contraseña Básica")
        self.num_generations = tk.IntVar(value=5)

        # --- Interfaz de Entrada ---
        input_frame = ttk.LabelFrame(self, text="Generación de Palabras (Tareas 07/10, 08/10)")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Fila 1: Selección de Gramática
        ttk.Label(input_frame, text="Seleccionar Gramática:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        grammar_options = list(self.grammars.keys())
        self.grammar_combobox = ttk.Combobox(input_frame, textvariable=self.selected_grammar, values=grammar_options, state="readonly")
        self.grammar_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Fila 2: Número de Generaciones
        ttk.Label(input_frame, text="Número de Ejemplos:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(input_frame, textvariable=self.num_generations, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        input_frame.grid_columnconfigure(1, weight=1) # Permite que el combobox se expanda

        # --- Botón de Ejecución ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(btn_frame, text="GENERAR PALABRAS", command=self.execute_generation).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="<- Volver al Menú Principal", command=controller.create_main_menu).pack(side="right", padx=5)

        # --- Interfaz de Salida ---
        output_frame = ttk.LabelFrame(self, text="Palabras Generadas")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def execute_generation(self):
        """Maneja la lógica de la Tarea 07/10 y 08/10: Generar palabras."""
        self.output_text.delete("1.0", tk.END)
        grammar_name = self.selected_grammar.get()
        grammar_data = self.grammars.get(grammar_name)
        num = self.num_generations.get()
        
        if grammar_data is None:
            self.output_text.insert(tk.END, f"ERROR: La gramática '{grammar_name}' aún no está implementada.\n")
            return
            
        try:
            generator = GrammarGenerator(grammar_data)
            self.output_text.insert(tk.END, f"Generando {num} ejemplos para: {grammar_name}\n")
            self.output_text.insert(tk.END, "-------------------------------------\n")
            
            for i in range(num):
                word = generator.generate(max_length=100) # Llama al módulo de generación
                self.output_text.insert(tk.END, f"{i+1}. {word}\n")
                
        except Exception as e:
            messagebox.showerror("Error de Generación", f"Ocurrió un error en el generador: {e}")
            self.output_text.insert(tk.END, f"ERROR: {e}\n")


if __name__ == "__main__":
    app = AutomaApp()
    app.mainloop()