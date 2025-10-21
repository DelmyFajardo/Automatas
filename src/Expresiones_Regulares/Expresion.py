
#Empieza el codigo k
from .input_handler import load_source_text, get_text_from_manual_input
from .regex_finder import find_patterns, MatchResult
from typing import List, Optional

class ExpresionSearcher:
    """
    Clase para manejar el flujo completo de una búsqueda de patrón.
    """
    def __init__(self, regex: str):
        self.regex = regex
        self.text_content: Optional[str] = None
        self.results: List[MatchResult] = []

    def load_text(self, source_identifier: Optional[str] = None) -> bool:
        """Carga el texto desde archivo, URL o pide entrada manual, con manejo de excepciones."""
        self.text_content = None # Inicializa o limpia el contenido anterior

        try:
            if source_identifier:
                # Intenta cargar desde archivo o URL
                self.text_content = load_source_text(source_identifier)
            else:
                # Asume entrada manual
                self.text_content = get_text_from_manual_input()
                # La línea de depuración que pusiste:
                # print("contenido"+self.text_content) 

            # Verificar si se cargó algo
            if self.text_content is None or len(self.text_content.strip()) == 0:
                print("ADVERTENCIA: La fuente no contiene texto o la carga falló silenciosamente.")
                return False
            
            return True

        except Exception as e:
            # Captura cualquier error no manejado por las funciones internas (como problemas de encoding o I/O inesperados)
            print(f"ERROR FATAL al cargar la fuente de texto: {e}")
            # NOTA: En la GUI, es mejor usar tkinter.messagebox.showerror en el método execute_search.
            return False

    def execute_search(self) -> List[MatchResult]:
        """Ejecuta la búsqueda si el texto ha sido cargado."""
        if not self.text_content:
            print("ERROR: No hay texto cargado para ejecutar la búsqueda.")
            return []
        
        # Llamada a la función del 06/10
        self.results = find_patterns(self.text_content, self.regex)
        
        # El requisito es listar las coincidencias, incluyendo el número de línea [cite: 17]
        self.list_results() 
        
        return self.results

    def list_results(self):
        """Muestra las coincidencias formateadas."""
        if not self.results:
            print("\nINFO: No se encontraron coincidencias para la expresión regular.")
            return

        print(f"\n--- Coincidencias encontradas ({len(self.results)}) ---")
        for res in self.results:
            print(f"Línea {res['line_num']:<4} Col {res['col_start']:<4}: '{res['match']}'")

# --- Próximo Paso: Integración en main.py ---
if __name__ == '__main__':
    # Simulación de un proceso de búsqueda
    test_regex = r'\d+' # Busca cualquier número

    print("--- 1. Búsqueda con Entrada Manual ---")
    searcher_manual = ExpresionSearcher(test_regex)
    if searcher_manual.load_text():
        searcher_manual.execute_search()
    
    # Puedes añadir aquí una prueba para URL o archivo si tienes datos disponibles
    # print("\n--- 2. Búsqueda con Archivo (simulación) ---")
    # searcher_file = ExpresionSearcher(r'[A-Z]{3,}')
    # if searcher_file.load_text("ruta/a/archivo.txt"):
    #     searcher_file.execute_search()