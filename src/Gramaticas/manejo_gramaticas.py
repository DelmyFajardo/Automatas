from typing import Dict, Any, Optional
from .gramaticas_db import crear_tabla_gramaticas, insertar_gramatica, obtener_todas_gramaticas


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
        "variables": ["S", "Local", "Nombre", "Apellido", "Digitos"],
        "terminales": list("abcdefghijklmnopqrstuvwxyz0123456789._-@"),
        "inicial": "S",
        "producciones": [
            ("S", ["Local", "@", "gmail.com"]),
            ("Local", ["Nombre", "Digitos"]),
            ("Local", ["Nombre", ".", "Apellido"]),
            ("Nombre", ["karla", "juan", "maria", "carlos", "ana", "luis", "marta", "jose", "miguel", "laura"]),
            ("Apellido", ["perez", "lopez", "gonzalez", "hernandez", "martinez", "ramirez", "ruiz", "sanchez"]),
            ("Digitos", ["D"]),
            ("Digitos", ["D", "D"]),
            ("Digitos", ["D", "D", "D"]),
            ("D", list("0123456789"))
        ]
    },
    "direccion": {
        "variables": ["S", "Tipo", "NombreVia", "Numero", "Zona", "Ciudad", "Depto", "D"],
        "terminales": list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-"),
        "inicial": "S",
        "producciones": [
            ("S", ["Tipo", " ", "NombreVia", " ", "Numero", ", Zona ", "Zona", ", ", "Ciudad", ", ", "Depto"]),
            ("Tipo", ["Avenida", "Calle", "Boulevard", "6a Avenida", "7a Calle", "3a Avenida"]),
            ("NombreVia", ["Real", "Principal", "Central", "Reforma", "San Jose", "Santa Ana", "La Paz", "Libertad", "Los Altos", "El Centro"]),
            ("Numero", ["D", "Numero", "-", "D"]),
            ("Numero", ["D"]),
            ("D", list("0123456789")),
            ("Zona", ["D", "D"]),
            ("Ciudad", ["Ciudad de Guatemala", "Mixco", "Villa Nueva", "Quetzaltenango", "Antigua Guatemala", "Escuintla", "Cobán", "Chimaltenango", "Huehuetenango", "San Marcos", "Jalapa", "Peten"]),
            ("Depto", ["Guatemala", "Guatemala", "Guatemala", "Quetzaltenango", "Sacatepequez", "Escuintla", "Alta Verapaz", "Chimaltenango", "Huehuetenango", "San Marcos", "Jalapa", "Petén"])
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
        "variables": ["S", "Nombre", "Apellido"],
        "terminales": list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ " ),
        "inicial": "S",
        "producciones": [
            ("S", ["Nombre", " ", "Apellido"]),
            ("Nombre", ["Karla", "Juan", "María", "Carlos", "Ana", "Luis", "Marta", "José", "Miguel", "Laura"]),
            ("Apellido", ["Pérez", "López", "González", "Hernández", "Martínez", "Ramírez", "Ruiz", "Sánchez"])
        ]
    }
}

def seleccionar_gramatica(nombre: str, gramaticas: Optional[Dict[str, Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    if gramaticas is None:
        gramaticas = GRAMATICAS_PREDEFINIDAS
    return gramaticas.get(nombre)


try:
    crear_tabla_gramaticas()
  
    for nombre, gr in GRAMATICAS_PREDEFINIDAS.items():
        try:
            insertar_gramatica(nombre, gr)
        except Exception:
            pass
    try:
        existentes = obtener_todas_gramaticas()
        if existentes:
            GRAMATICAS_PREDEFINIDAS.clear()
            GRAMATICAS_PREDEFINIDAS.update(existentes)
    except Exception:
        pass
except Exception:
    pass

