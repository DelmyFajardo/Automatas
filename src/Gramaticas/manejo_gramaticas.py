from typing import Dict, Any, Optional


GRAMATICAS_PREDEFINIDAS: Dict[str, Dict[str, Any]] = {
    "contraseña": {
        "variables": ["S", "L", "D"],
        "terminales": list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"),
        "inicial": "S",
        "producciones": [
            ("S", ["L", "D", "L"]),
            ("L", list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")),
            ("D", list("0123456789!@#$%"))
        ]
    },
    "correo": {
        "variables": ["S", "U", "D", "E"],
        "terminales": list("abcdefghijklmnopqrstuvwxyz0123456789._-@"),
        "inicial": "S",
        "producciones": [
            ("S", ["U", "@", "D", ".", "E"]),
            ("U", list("abcdefghijklmnopqrstuvwxyz0123456789._-")),
            ("D", list("abcdefghijklmnopqrstuvwxyz")),
            ("E", ["com", "net", "org"])
        ]
    },
    "direccion": {
        "variables": ["S", "N", "C"],
        "terminales": list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "),
        "inicial": "S",
        "producciones": [
            ("S", ["C", " ", "N"]),
            ("C", list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")),
            ("N", list("0123456789"))
        ]
    },
    "telefono": {
        "variables": ["S", "D"],
        "terminales": list("0123456789-+() "),
        "inicial": "S",
        "producciones": [
            ("S", ["+", "D", " ", "D", "-", "D"]),
            ("D", list("0123456789"))
        ]
    },
    "usuario": {
        "variables": ["S", "L"],
        "terminales": list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"),
        "inicial": "S",
        "producciones": [
            ("S", ["L", "L", "L"]),
            ("L", list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"))
        ]
    }
}

def seleccionar_gramatica(nombre: str, gramaticas: Optional[Dict[str, Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    if gramaticas is None:
        gramaticas = GRAMATICAS_PREDEFINIDAS
    return gramaticas.get(nombre)
