# Importar módulos necesarios (asumiendo que ExpresionSearcher está en Expresiones_Regulares)
from src.Expresiones_Regulares.Expresion import ExpresionSearcher 
# Necesitas crear un módulo GramaticaGenerator o similar en src/Gramaticas

def display_menu():
    """Muestra el menú principal de la aplicación."""
    print("\n--- PROYECTO AUTÓMATAS ---")
    print("1. Búsqueda de Patrones (Regex)")
    print("2. Generación de Palabras (Gramáticas)")
    print("3. Salir")
    return input("Seleccione una opción (1-3): ")

def handle_regex_search():
    """Maneja la lógica de búsqueda con Regex."""
    print("\n--- Búsqueda de Patrones ---")
    regex = input("Ingrese la Expresión Regular: ").strip()
    source = input("Ingrese la ruta del archivo, URL, o presione Enter para entrada manual: ").strip()
    
    if not regex:
        print("ERROR: La expresión regular no puede estar vacía.")
        return

    # La lógica de ExpresionSearcher cubre Tareas 04/10, 05/10, 07/10
    searcher = ExpresionSearcher(regex)
    
    # load_text con source si se ingresó, o None para entrada manual
    if searcher.load_text(source if source else None):
        searcher.execute_search()

def main():
    """Función principal del CLI."""
    while True:
        choice = display_menu()
        if choice == '1':
            handle_regex_search()
        elif choice == '2':
            # Implementar Generación de Gramáticas aquí (Tareas 07/10, 08/10)
            print("Funcionalidad de Generación de Gramáticas Pendiente...")
        elif choice == '3':
            print("Saliendo del proyecto. ¡Éxitos!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == '__main__':
    # Asegúrate de haber instalado 'requests' si no lo has hecho.
    main()