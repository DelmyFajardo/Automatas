
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
        self.text_content = None 

        try:
            if source_identifier:
                self.text_content = load_source_text(source_identifier)
            else:
                self.text_content = get_text_from_manual_input()
               
            if self.text_content is None or len(self.text_content.strip()) == 0:
                print("ADVERTENCIA: La fuente no contiene texto o la carga falló silenciosamente.")
                return False
            
            return True

        except Exception as e:
            print(f"ERROR FATAL al cargar la fuente de texto: {e}")
            return False

    def execute_search(self) -> List[MatchResult]:
        """Ejecuta la búsqueda si el texto ha sido cargado."""
        if not self.text_content:
            print("ERROR: No hay texto cargado para ejecutar la búsqueda.")
            return []
        
        self.results = find_patterns(self.text_content, self.regex)
        
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

if __name__ == '__main__':
    test_regex = r'\d+' 
    print("--- 1. Búsqueda con Entrada Manual ---")
    searcher_manual = ExpresionSearcher(test_regex)
    if searcher_manual.load_text():
        searcher_manual.execute_search()
    