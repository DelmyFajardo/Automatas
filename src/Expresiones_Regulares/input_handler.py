import os
import sys
from typing import Optional

# Dependencia para URLs (Necesitas 'pip install requests')
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Advertencia: La librería 'requests' no está instalada. La lectura de URLs estará deshabilitada.")


def read_text_from_file(file_path: str) -> Optional[str]:
    """Lee el contenido de un archivo local (parte de la Tarea 05/10)."""
    if not os.path.exists(file_path):
        print(f"ERROR: Archivo no encontrado en la ruta: {file_path}")
        return None
    try:
        # Usar 'utf-8' es estándar y robusto
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f"INFO: Archivo '{file_path}' leído correctamente.")
            return f.read()
    except IOError as e:
        print(f"ERROR I/O al leer el archivo '{file_path}': {e}")
        return None

def read_text_from_url(url: str) -> Optional[str]:
    """Descarga el contenido de una URL (Tarea 07/10)."""
    if not HAS_REQUESTS:
        print("ERROR: La lectura de URL requiere la librería 'requests'.")
        return None
    
    # Validación básica de la URL (más estricta se haría con urllib.parse)
    if not url.lower().startswith(('http://', 'https://')):
        print(f"ERROR: La cadena '{url}' no parece una URL válida.")
        return None

    try:
        # Añadir un timeout es crucial en operaciones de red
        response = requests.get(url, timeout=15) 
        # Asegura que el código de estado sea 200 (OK)
        response.raise_for_status() 

        return response.text 
    except requests.exceptions.RequestException as e:
        # Captura todos los errores de request (conexión, timeout, HTTP)
        print(f"ERROR de red al acceder a la URL: {e}")
        return None

def get_text_from_manual_input(prompt: str = "Ingrese el texto a analizar (finalice con Ctrl+D o una línea vacía):") -> str:
    """Lee texto multilínea de la entrada estándar (parte de la Tarea 05/10)."""
    print(prompt)
    lines = []
    # Loop que termina al ingresar una línea vacía (en consola) o EOF (Ctrl+D/Z)
    try:
        while True:
            # sys.stdin.readline es más directo para entrada multilínea que input()
            line = sys.stdin.readline()
            if not line.strip(): # Permite terminar con línea vacía
                break
            lines.append(line.rstrip('\n')) # Mantener los '\n' originales si es necesario
    except EOFError:
        pass # Termina si se presiona EOF

    # Unimos las líneas con '\n' para formar el bloque de texto original
    return '\n'.join(lines)


def load_source_text(source_identifier: str) -> Optional[str]:
    """
    Función unificada para cargar texto basado en el identificador.
    Prioridad: 1. Archivo Local -> 2. URL -> 3. Texto Directo (no aplica para esta función)
    """
    print(f"INFO: Cargando texto desde: {source_identifier}")
    if os.path.exists(source_identifier):
        print(f"INFO: Leyendo de archivo local: {source_identifier}")
        return read_text_from_file(source_identifier)
    
    if source_identifier.lower().startswith(('http://', 'https://')):
        print(f"INFO: Intentando descargar de URL: {source_identifier}")
        return read_text_from_url(source_identifier)
    
    # Si no es archivo ni URL, devolvemos la cadena como texto directo
    return source_identifier

if __name__ == '__main__':
    # Simulación de prueba para la entrada manual
    print("--- Prueba de Entrada Manual ---")
    manual_text = get_text_from_manual_input()
    print("\n--- Texto Leído ---")
    print(manual_text)