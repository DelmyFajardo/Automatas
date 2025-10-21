import random
from typing import Dict, List, Optional

# Definición de las producciones de la Gramática 1 (Ejemplo simplificado)
GRAMATICA_CONTRASENA = {
    "nombre": "ContrasenaBasica",
    "simbolo_inicial": "<Password>",
    "producciones": {
        "<Password>": ["<Parte1><Parte2>"], # Mínimo 8 caracteres
        "<Parte1>": ["<Letra>", "<Numero>", "<Simbolo>"],
        "<Parte2>": ["", "<Parte1><Parte2>"],
        
        # Terminales con rangos
        "<Letra>": [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                   [chr(i) for i in range(ord('A'), ord('Z') + 1)],
        "<Numero>": [str(i) for i in range(10)],
        "<Simbolo>": ["!", "@", "#", "$", "%"]
    }
}


GRAMATICA_EMAIL = {
    "nombre": "CorreoElectronicoBasico",
    "simbolo_inicial": "<Email>",
    "producciones": {
        "<Email>": [
            "<LocalPart>@<DomainPart>.<TLD>"
        ],
        
        # --- Parte Local (Nombre de usuario) ---
        # Permite letras/numeros, punto (.), y guion bajo (_)
        "<LocalPart>": [
            "<LocalChar>", 
            "<LocalPart><LocalChar>",
            "<LocalPart><LocalSep>" # Permite separadores internos
        ],
        
        # Símbolos terminales permitidos en la Parte Local (ej: usuario.nombre_123)
        "<LocalChar>": [
            * [chr(i) for i in range(ord('a'), ord('z') + 1)], # Letras minúsculas
            * [str(i) for i in range(10)],                     # Números
        ],
        "<LocalSep>": [
            ".", "_"
        ],

        # --- Parte Dominio ---
        # El dominio puede ser multinivel (ej: sub.dominio.com)
        "<DomainPart>": [
            "<DomainSub>",
            "<DomainSub>.<DomainPart>" # Recursividad para subdominios
        ],
        "<DomainSub>": [
            "<DomainChar>", 
            "<DomainSub><DomainChar>" # Mínimo un caracter
        ],
        
        # Símbolos terminales permitidos en la Parte Dominio (solo letras y números)
        "<DomainChar>": [
            * [chr(i) for i in range(ord('a'), ord('z') + 1)],
            * [str(i) for i in range(10)],
        ],
        
        # --- TLD (Top-Level Domain) ---
        "<TLD>": [
            "com", "net", "org", "co", "io", "gob"
        ]
    }
}

GRAMATICA_IPV4 = {
    "nombre": "DireccionIPv4",
    "simbolo_inicial": "<IPv4>",
    "producciones": {
        "<IPv4>": [
            "<Octeto>.<Octeto>.<Octeto>.<Octeto>"
        ],
        
        # --- Octeto (Representa un número entre 0 y 255) ---
        # Dividido en reglas para aproximar el rango 0-255.
        "<Octeto>": [
            # 1. Números de 1 o 2 dígitos (0-99)
            "<Cifra>", 
            "<Cifra><Cifra>", 
            
            # 2. Números de 100 a 199
            "1<Cifra><Cifra>", 
            
            # 3. Números de 200 a 249
            "2<Cifra20_49>", 
            
            # 4. Números de 250 a 255
            "25<Cifra0_5>" 
        ],
        
        # Terminales: Cifras
        "<Cifra>": [str(i) for i in range(10)],             # 0 a 9
        "<Cifra20_49>": [str(i) for i in range(10)],        # 0 a 9 (para 200-209, 210-219, etc.)
        "<Cifra0_5>": [str(i) for i in range(6)],           # 0 a 5
        
        # Nota: La regla de 200 a 249 se simplifica como 2XX. La lógica real 
        # (200-249) es más compleja y se controla mejor con la longitud máxima.
        # Si quieres más precisión:
        # "2<Cifra0_4><Cifra>",  # 200-249
        # "<Cifra0_4>": [str(i) for i in range(5)], # 0 a 4
    }
}



class GrammarGenerator:
    def __init__(self, grammar_data: Dict):
        self.productions = grammar_data["producciones"]
        self.start_symbol = grammar_data["simbolo_inicial"]
        self.terminales = self._identify_terminals()

    def _identify_terminals(self) -> List[str]:
        """Identifica los símbolos que no son no-terminales."""
        non_terminals = set(self.productions.keys())
        terminals = set()
        for rules in self.productions.values():
            for rule in rules:
                for symbol in self._get_symbols_from_rule(rule):
                    if symbol not in non_terminals and symbol != "":
                        terminals.add(symbol)
        return list(terminals)
    
    def _get_symbols_from_rule(self, rule: str) -> List[str]:
        """Divide una regla de producción en sus símbolos constituyentes."""
        # Esto requiere una implementación más sofisticada para reconocer símbolos 
        # rodeados por < >. Por ahora, asumiremos que los símbolos no-terminales 
        # están separados o al inicio/final.
        
        # Implementación simple: si contiene '<', es no-terminal, si no, es terminal.
        symbols = []
        current_symbol = ""
        in_nt = False
        for char in rule:
            if char == '<':
                if current_symbol:
                    symbols.append(current_symbol)
                current_symbol = '<'
                in_nt = True
            elif char == '>':
                current_symbol += '>'
                symbols.append(current_symbol)
                current_symbol = ""
                in_nt = False
            elif in_nt:
                current_symbol += char
            else:
                # Si no estamos dentro de un NT, el carácter es un terminal
                symbols.append(char)
        
        if current_symbol and not in_nt: # Si quedó un terminal al final
             symbols.append(current_symbol)
             
        # NOTA TÉCNICA: La derivación recursiva es más fácil si cada regla es una
        # lista de sus símbolos (ej. ["<Letra>", "<Numero>"]).

        # Para esta implementación, usaremos una simple lista de caracteres para 
        # terminales y la cadena completa para no-terminales.
        
        # Una alternativa más fácil es reemplazar solo el primer NT encontrado 
        # en la cadena a derivar.
        return [rule] # Devolvemos la regla completa para un manejo más simple.

    def generate(self, max_length: int = 15) -> str:
        """Realiza una derivación aleatoria para generar una palabra."""
        work_string = self.start_symbol
        steps = 0
        
        while any(nt in work_string for nt in self.productions) and steps < 1000:
            steps += 1
            
            # Buscar el primer No Terminal (NT)
            nt_start = work_string.find('<')
            if nt_start == -1:
                break # Solo quedan terminales
            
            nt_end = work_string.find('>', nt_start)
            if nt_end == -1:
                break # Error de gramática
                
            nt_symbol = work_string[nt_start : nt_end + 1]

            if nt_symbol in self.productions:
                # 1. Selecciona una producción de forma aleatoria
                selected_rule = random.choice(self.productions[nt_symbol])
                
                # 2. Reemplaza el NT por la regla seleccionada
                work_string = work_string[:nt_start] + selected_rule + work_string[nt_end + 1:]
                
                # Control de longitud (para evitar bucles infinitos en gramáticas recursivas)
                if len(work_string) > max_length * 2:
                    print("Advertencia: Palabra excedió el límite de longitud. Deteniendo.")
                    break
            else:
                print(f"Error: Símbolo No Terminal desconocido '{nt_symbol}'")
                break
                
        return work_string.replace("<", "").replace(">", "") # Limpia los símbolos NT

if __name__ == '__main__':
    # Tarea 07/10: Primera gramática (Contraseña)
    generator1 = GrammarGenerator(GRAMATICA_CONTRASENA)
    print("--- Generación de Contraseñas ---")
    for _ in range(5):
        print(f"Generada: {generator1.generate(max_length=10)}")

    # Tarea 08/10: Implementar 2 gramáticas más aquí.
    
    # Gramática 2: Nombres de Usuario (Ejemplo simplificado)
  