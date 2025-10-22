import random
from typing import Dict, List, Optional


# ----------------------------------------------------------------------
# DEFINICIONES DE GRAMÁTICAS (Incluyendo Correcciones para GT)
# ----------------------------------------------------------------------

# Gramática 1: Contraseña (CORREGIDA - SEGURA)
GRAMATICA_CONTRASENA = {
    "nombre": "ContrasenaSegura",
    "simbolo_inicial": "<Password>",
    "producciones": {
        # 1. <Password> garantiza la inclusión de los 3 tipos de caracteres obligatorios 
        #    en orden aleatorio inicial, seguido por el cuerpo.
        "<Password>": [
            "<Letra><Numero><Simbolo><Cuerpo>",
            "<Numero><Simbolo><Letra><Cuerpo>",
            "<Simbolo><Letra><Numero><Cuerpo>",
            "<Letra><Simbolo><Numero><Cuerpo>",
            "<Numero><Letra><Simbolo><Cuerpo>",
            "<Simbolo><Numero><Letra><Cuerpo>"
        ], 
        
        # 2. <Cuerpo> genera el resto de la contraseña de forma recursiva (puede ser vacío).
        "<Cuerpo>": [
            "",                             # Producción vacía para terminar la recursión
            "<Componente><Cuerpo>"          # Agrega un carácter y continúa
        ],
        
        # 3. <Componente> es cualquier carácter permitido.
        "<Componente>": [
            "<Letra>", 
            "<Numero>", 
            "<Simbolo>"
        ],

        # 4. Terminales
        "<Letra>": [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                   [chr(i) for i in range(ord('A'), ord('Z') + 1)],
        "<Numero>": [str(i) for i in range(10)],
        # Más símbolos para mayor seguridad
        "<Simbolo>": ["!", "@", "#", "$", "%", "&", "*", "-", "+", "="]
    }
}

# Gramática 2: Correo Electrónico
GRAMATICA_EMAIL = {
    "nombre": "CorreoElectronicoBasico",
    "simbolo_inicial": "<Email>",
    "producciones": {
        # La forma correcta de escribir NTs en la producción es la clave:
        "<Email>": ["<LocalPart>@<DomainPart>.<TLD>"],
        "<LocalPart>": ["<LocalChar>", "<LocalPart><LocalChar>", "<LocalPart><LocalSep>"],
        "<LocalChar>": [*[chr(i) for i in range(ord('a'), ord('z') + 1)], *[str(i) for i in range(10)]],
        "<LocalSep>": [".", "_"],
        "<DomainPart>": ["<DomainSub>", "<DomainSub>.<DomainPart>"],
        "<DomainSub>": ["<DomainChar>", "<DomainSub><DomainChar>"],
        "<DomainChar>": [*[chr(i) for i in range(ord('a'), ord('z') + 1)], *[str(i) for i in range(10)]],
        "<TLD>": ["com", "net", "org", "co", "io", "gob"]
    }
}

# Gramática 3: Dirección IPv4
GRAMATICA_IPV4 = {
    "nombre": "DireccionIPv4",
    "simbolo_inicial": "<IPv4>",
    "producciones": {
        "<IPv4>": ["<Octeto>.<Octeto>.<Octeto>.<Octeto>"],
        "<Octeto>": ["<Cifra>", "<Cifra><Cifra>", "1<Cifra><Cifra>", "2<Cifra20_49>", "25<Cifra0_5>"],
        "<Cifra>": [str(i) for i in range(10)], 
        "<Cifra20_49>": [str(i) for i in range(10)], 
        "<Cifra0_5>": [str(i) for i in range(6)], 
    }
}

# Gramática 4: Dirección Postal (CORREGIDA para formato GT)
# Gramática 4: Dirección Postal (CORREGIDA, Anti-Recursividad)
GRAMATICA_DIRECCION = {
    "nombre": "DireccionPostalGT",
    "simbolo_inicial": "<S>",
    "producciones": {
        # Formato: 'Tipo de Vía # - #, Zona Z, Ciudad, Depto'
        "<S>": [
            "<Tipo> <NumeroVia>-<NumeroCasa>, Zona <Zona>, <Ciudad>, <Depto>"
        ],
        "<Tipo>": [
            "Avenida", "Calle", "Boulevard", "6a Avenida", "7a Calle", "3a Avenida"
        ],
        
        # Eliminamos la recursividad en el número de vía. 
        # Ahora solo genera un número de 1 a 2 dígitos.
        "<NumeroVia>": [
            "<D>",      # Ej: '1'
            "<D><D>"    # Ej: '12'
        ],
        
        # Número de Casa/Guion (ej: 01, 80). Eliminamos la recursividad.
        "<NumeroCasa>": [
            "<D><D>",
            "<D>"
        ],
        
        # Dígitos
        "<D>": [str(i) for i in range(10)],
        
        # Zona (simula 1-25)
        "<Zona>": [
            "0<Cifra1_9>",
            "1<Cifra0_9>",
            "2<Cifra0_5>"
        ],
        "<Cifra0_9>": [str(i) for i in range(10)],
        "<Cifra1_9>": [str(i) for i in range(1, 10)],
        "<Cifra0_5>": [str(i) for i in range(6)],
        
        "<Ciudad>": [
            "Ciudad de Guatemala", "Mixco", "Villa Nueva", "Quetzaltenango", "Antigua Guatemala", 
            "Escuintla", "Cobán", "Chimaltenango", "Huehuetenango", "San Marcos", "Jalapa", "Peten"
        ],
        "<Depto>": [
            "Guatemala", "Quetzaltenango", "Sacatepequez", "Escuintla", 
            "Alta Verapaz", "Chimaltenango", "Huehuetenango", "San Marcos", "Jalapa", "Petén"
        ]
    }
}

# Gramática 5: Teléfono (CORREGIDA para formato GT)
GRAMATICA_TELEFONO = {
    "nombre": "NumeroTelefonoGT",
    "simbolo_inicial": "<S>",
    "producciones": {
        # Formato: XXXX-XXXX (8 dígitos, común en GT)
        # Nota: Usamos <D> en lugar de <Digito> por simplicidad y consistencia
        "<S>": ["<D><D><D><D>-<D><D><D><D>"],
        "<D>": [str(i) for i in range(10)], # 0-9
    }
}

# Gramática 6: Usuario (Generación de Nombres)
GRAMATICA_USUARIO = {
    "nombre": "NombreCompleto",
    "simbolo_inicial": "<S>",
    "producciones": {
        "<S>": ["<Nombre> <Apellido>"],
        "<Nombre>": ["Karla", "Juan", "María", "Carlos", "Ana", "Luis", "Marta", "José", "Miguel", "Laura"],
        "<Apellido>": ["Pérez", "López", "González", "Hernández", "Martínez", "Ramírez", "Ruiz", "Sánchez"]
    }
}


class GrammarGenerator:
    def __init__(self, grammar_data: Dict):
        self.productions = grammar_data["producciones"]
        self.start_symbol = grammar_data["simbolo_inicial"]
        self.non_terminals = set(self.productions.keys())
        # Nota: _identify_terminals es redundante si solo usamos el mapeo de producciones

    # NO es necesario cambiar _identify_terminals ni _get_symbols_from_rule
    
    def generate(self, max_length: int = 50) -> str:
        """
        Realiza una derivación aleatoria para generar una palabra.
        Asegura que todos los NTs se expandan.
        """
        work_string = self.start_symbol
        steps = 0
        
        # Continuar mientras haya símbolos No Terminales (<...>) y no excedamos los pasos
        while any(nt in work_string for nt in self.productions) and steps < 1000:
            steps += 1
            
            # --- Lógica de Búsqueda y Reemplazo del PRIMER NT ---
            
            nt_start = work_string.find('<')
            if nt_start == -1: break 
            
            nt_end = work_string.find('>', nt_start)
            if nt_end == -1: break 
                
            nt_symbol = work_string[nt_start : nt_end + 1]

            if nt_symbol in self.productions:
                # 1. Selecciona una producción de forma aleatoria
                selected_rule = random.choice(self.productions[nt_symbol])
                
                # 2. Reemplaza el NT por la regla seleccionada
                work_string = work_string[:nt_start] + selected_rule + work_string[nt_end + 1:]
                
                # Control de longitud (usando solo terminales)
                if len(work_string.replace('<','').replace('>','')) > max_length:
                    return f"ERROR: Límite de longitud ({max_length}) excedido o recursión excesiva."
            else:
                # Esto captura un NT que está en la cadena pero no en la producción (un error de gramática)
                return f"ERROR: Símbolo No Terminal no definido: {nt_symbol}"
                
        # Limpia cualquier NT remanente (aunque no debería haber si el bucle terminó bien)
        return work_string.replace("<", "").replace(">", "")


# ----------------------------------------------------------------------
# PRUEBA DE GENERACIÓN (Bloque principal de ejecución)
# ----------------------------------------------------------------------
if __name__ == '__main__':
    
    print("--- 1. Generación de Contraseñas ---")
    generator1 = GrammarGenerator(GRAMATICA_CONTRASENA)
    for _ in range(3):
        print(f"Generada: {generator1.generate(max_length=12)}")
        
    print("\n--- 2. Generación de Correos Electrónicos ---")
    generator2 = GrammarGenerator(GRAMATICA_EMAIL)
    for _ in range(3):
        print(f"Generada: {generator2.generate(max_length=30)}")
        
    print("\n--- 3. Generación de Direcciones IPv4 ---")
    generator3 = GrammarGenerator(GRAMATICA_IPV4)
    for _ in range(3):
        print(f"Generada: {generator3.generate(max_length=15)}")

    print("\n--- 4. Generación de Direcciones Postales (CORREGIDA) ---")
    generator4 = GrammarGenerator(GRAMATICA_DIRECCION)
    for _ in range(3):
        print(f"Generada: {generator4.generate(max_length=80)}")

    print("\n--- 5. Generación de Teléfonos GT (CORREGIDA) ---")
    generator5 = GrammarGenerator(GRAMATICA_TELEFONO)
    for _ in range(3):
        print(f"Generada: {generator5.generate(max_length=9)}")
        
    print("\n--- 6. Generación de Nombres de Usuario/Personas ---")
    generator6 = GrammarGenerator(GRAMATICA_USUARIO)
    for _ in range(3):
        print(f"Generada: {generator6.generate(max_length=20)}")