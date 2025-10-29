import re
from typing import List, Dict, Tuple

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
    
    try:
        compiled_regex = re.compile(regex)
    except re.error as e:
        print(f"ERROR: Expresión regular inválida: {e}")
        return results
    for line_num, line in enumerate(text.splitlines(), start=1):
        for match in compiled_regex.finditer(line):
            results.append({
                'match': match.group(0),    
                'line_num': line_num,       
                'col_start': match.start() + 1 
            })

    return results

if __name__ == '__main__':
    sample_text = """
    Email de prueba: user.123@dominio.com
    Otro email: admin@empresa.net
    Sin email aquí.
    user@host.org, otro@mail.co.uk
    """
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 

    coincidences = find_patterns(sample_text, email_regex)

    print(f"Regex utilizada: {email_regex}\n")
    for res in coincidences:
        print(f"Línea {res['line_num']}, Columna {res['col_start']}: '{res['match']}'") 
        