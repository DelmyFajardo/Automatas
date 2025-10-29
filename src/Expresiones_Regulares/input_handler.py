import os
import sys
from typing import Optional

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
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    
    
    if not url.lower().startswith(('http://', 'https://')):
        print(f"ERROR: La cadena '{url}' no parece una URL válida.")
        return None

    try:
        response = requests.get(url, headers=headers, timeout=15) 
        response.raise_for_status() 

        print(f"INFO: Solicitud a {url} exitosa.")
        return response.text 
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR de red al acceder a la URL: {url}. Detalle: {e}")
        return None

def get_text_from_manual_input(prompt: str = "Ingrese el texto a analizar (finalice con Ctrl+D o una línea vacía):") -> str:
    """Lee texto multilínea de la entrada estándar (parte de la Tarea 05/10)."""
    print(prompt)
    lines = []
    try:
        while True:
            line = sys.stdin.readline()
            if not line.strip(): 
                break
            lines.append(line.rstrip('\n')) 
    except EOFError:
        pass 
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
    
    return source_identifier

if __name__ == '__main__':
    print("--- Prueba de Entrada Manual ---")
    manual_text = get_text_from_manual_input()
    print("\n--- Texto Leído ---")
    print(manual_text)