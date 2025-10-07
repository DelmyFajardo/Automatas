import re
from typing import List, Dict, Tuple

# La salida debe incluir la coincidencia, el índice (columna) y la línea.
MatchResult = Dict[str, any]

def find_patterns(text: str, regex: str) -> List[MatchResult]:
    """
    Busca patrones de regex en un texto de múltiples líneas.

    Args:
        text (str): El texto de entrada completo.
        regex (str): La expresión regular a buscar.

    Returns:
        List[MatchResult]: Una lista de diccionarios con las coincidencias.
                           Cada dict: {'match': str, 'line_num': int, 'col_start': int}
    """
    results: List[MatchResult] = []
    
    # Compilar la regex para eficiencia, especialmente si se va a reusar
    try:
        compiled_regex = re.compile(regex)
    except re.error as e:
        # Manejo de errores para regex mal formadas
        print(f"ERROR: Expresión regular inválida: {e}")
        return results

    # Iterar sobre las líneas del texto para obtener el número de línea.
    # enumerate(text.splitlines()): (0, 'primera línea'), (1, 'segunda línea'), ...
    for line_num, line in enumerate(text.splitlines(), start=1):
        # re.finditer encuentra todas las subcadenas no superpuestas que 
        # coinciden con el patrón en la línea.
        for match in compiled_regex.finditer(line):
            results.append({
                'match': match.group(0),    # El texto de la coincidencia
                'line_num': line_num,       # Número de línea (base 1)
                'col_start': match.start() + 1 # Columna de inicio (base 1)
            })

    return results

# --- Ejemplo de uso (Para pruebas iniciales) ---
if __name__ == '__main__':
    sample_text = """
    Email de prueba: user.123@dominio.com
    Otro email: admin@empresa.net
    Sin email aquí.
    user@host.org, otro@mail.co.uk
    """
    # Regex para encontrar un email básico
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 

    coincidences = find_patterns(sample_text, email_regex)

    print(f"Regex utilizada: {email_regex}\n")
    for res in coincidences:
        print(f"Línea {res['line_num']}, Columna {res['col_start']}: '{res['match']}'") 
        