from typing import List, Dict, Any
import random
from manejo_gramaticas import GRAMATICAS_PREDEFINIDAS
import re
import palabras_generadas_db
import secrets
import string


def _es_terminal(simbolo: str, gramatica: Dict[str, Any]) -> bool:
   
    producciones = gramatica.get('producciones', [])
    if any(prod[0] == simbolo for prod in producciones):
        return False
    return True


def generar_palabra(gramatica: Dict[str, Any], max_tokens: int = 12, rng: random.Random | None = None) -> str:
    
    if rng is None:
        rng = random

    def expandir(simbolo: str, tokens_left: int) -> str:
        if tokens_left <= 0:
            return ''

        if _es_terminal(simbolo, gramatica):
            return str(simbolo)

        producciones = [prod for prod in gramatica.get('producciones', []) if prod[0] == simbolo]
        if not producciones:
            return ''

        prod = rng.choice(producciones)
        rhs = prod[1]

        rhs_all_str = all(isinstance(x, str) for x in rhs)
        rhs_has_var = any(isinstance(x, str) and any(p[0] == x for p in gramatica.get('producciones', [])) for x in rhs)

        if rhs_all_str and not rhs_has_var:
            if all(len(x) == 1 for x in rhs):
                return rng.choice(rhs)
            return rng.choice(rhs)

        resultado = ''
        for s in rhs:
            if isinstance(s, list):
                if not s:
                    continue
                elegido = rng.choice(s)
                if any(p[0] == elegido for p in gramatica.get('producciones', [])):
                    resultado += expandir(elegido, tokens_left - 1)
                else:
                    resultado += str(elegido)
            elif isinstance(s, str):
                if any(p[0] == s for p in gramatica.get('producciones', [])):
                    resultado += expandir(s, tokens_left - 1)
                else:
                    resultado += str(s)
            else:
                resultado += str(s)

        return resultado

    return expandir(gramatica.get('inicial'), max_tokens)


def generar_varias(gramatica_nombre: str, cantidad: int, max_tokens: int = 12) -> List[str]:
    gr = GRAMATICAS_PREDEFINIDAS.get(gramatica_nombre)
    if not gr:
        raise ValueError(f"Gramática '{gramatica_nombre}' no encontrada")
    rng = random.Random()
    palabras: List[str] = []

    if gramatica_nombre == 'telefono':
        for _ in range(cantidad):
            palabras.append(_generar_telefono_guatemala(rng))
        return palabras

    for _ in range(cantidad):
        palabras.append(generar_palabra(gr, max_tokens=max_tokens, rng=rng))
    return palabras


def _generar_telefono_guatemala(rng: random.Random) -> str:
    digits = ''.join(rng.choice('0123456789') for _ in range(8))
    return f"+502 {digits}"


def generar_usuarios_personalizados(cantidad: int, min_len: int = 3, max_len: int = 12, rng: random.Random | None = None) -> List[str]:
    if rng is None:
        rng = random

    gr = GRAMATICAS_PREDEFINIDAS.get('usuario')
    if not gr:
        raise ValueError("Gramática 'usuario' no encontrada")

    resultados: List[str] = []
    usados = set()
    attempts_per_item = 200

    for _ in range(cantidad):
        generado = None
        for intento in range(attempts_per_item):
            candidato = generar_palabra(gr, max_tokens=max_len, rng=rng)
            if not candidato:
                continue
            candidato = str(candidato).strip()
            if len(candidato) < min_len or len(candidato) > max_len:
                continue
            if candidato in usados:
                continue
            generado = candidato
            usados.add(generado)
            break

        if generado is None:
            termos = gr.get('terminales', list('abcdefghijklmnopqrstuvwxyz0123456789._-'))
            length = min_len
            candidato = ''.join(rng.choice(termos) for _ in range(length))
            suffix = 1
            base = candidato
            while candidato in usados:
                candidato = f"{base}{suffix}"
                suffix += 1
            generado = candidato
            usados.add(generado)

        resultados.append(generado)

    return resultados


def generar_contrasenas_seguras(cantidad: int, length: int = 12, require_upper: bool = True, require_lower: bool = True, require_digit: bool = True, require_special: bool = True) -> List[str]:
    alphabet = ''
    if require_lower:
        alphabet += string.ascii_lowercase
    if require_upper:
        alphabet += string.ascii_uppercase
    if require_digit:
        alphabet += string.digits
    if require_special:
        alphabet += '!@#$%'

    if not alphabet:
        alphabet = string.ascii_letters + string.digits

    resultados: List[str] = []
    usados = set()

    for _ in range(cantidad):
        for intento in range(200):
            pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
            if require_lower and not any(c in string.ascii_lowercase for c in pwd):
                continue
            if require_upper and not any(c in string.ascii_uppercase for c in pwd):
                continue
            if require_digit and not any(c in string.digits for c in pwd):
                continue
            if require_special and not any(c in '!@#$%' for c in pwd):
                continue
            if pwd in usados:
                continue
            usados.add(pwd)
            resultados.append(pwd)
            break
        else:
            fallback = ''.join(random.choice(alphabet) for _ in range(length))
            resultados.append(fallback)

    return resultados


def validar_generado(nombre: str, palabra: str) -> bool:
    if palabra is None:
        return False
    if nombre == 'usuario':
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,}", palabra))
    if nombre == 'correo':
        return bool(re.fullmatch(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}", palabra))
    if nombre == 'direccion':
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .,#-]{5,}", palabra))
    if nombre == 'contraseña':
        return bool(re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%]{6,}", palabra))
    if nombre == 'telefono':
        return bool(re.fullmatch(r"[\d\-+() ]{8,}", palabra))
    return bool(palabra)


def generar_por_parametros(parametros: Dict[str, int], max_tokens_map: Dict[str, int] | None = None, attempts_per_item: int = 50, save: bool = True) -> Dict[str, List[str]]:
    resultados: Dict[str, List[str]] = {}
    if max_tokens_map is None:
        max_tokens_map = {}

    for nombre, cantidad in parametros.items():
        if cantidad is None or cantidad <= 0:
            continue
        max_t = max_tokens_map.get(nombre, 20)
        obtenidas: List[str] = []
        failures = 0
        for _ in range(cantidad):
            success = False
            if nombre == 'contraseña':
                vals = generar_contrasenas_seguras(1, length=max_t)
                candidato = vals[0] if vals else None
                if candidato and validar_generado(nombre, candidato):
                    obtenidas.append(candidato)
                    success = True
            elif nombre == 'usuario':
                vals = generar_usuarios_personalizados(1, min_len=3, max_len=max_t)
                candidato = vals[0] if vals else None
                if candidato and validar_generado(nombre, candidato):
                    obtenidas.append(candidato)
                    success = True
            elif nombre == 'direccion':
                vals = generar_varias('direccion', 1, max_tokens=max_t)
                candidato = vals[0] if vals else None
                if candidato and validar_generado(nombre, candidato):
                    obtenidas.append(candidato)
                    success = True
            elif nombre == 'telefono':
                vals = generar_varias('telefono', 1, max_tokens=max_t)
                candidato = vals[0] if vals else None
                if candidato and validar_generado(nombre, candidato):
                    obtenidas.append(candidato)
                    success = True
            else:
                for intento in range(attempts_per_item):
                    candidato = generar_palabra(GRAMATICAS_PREDEFINIDAS[nombre], max_tokens=max_t)
                    if validar_generado(nombre, candidato):
                        obtenidas.append(candidato)
                        success = True
                        break

            if not success:
                failures += 1
        resultados[nombre] = obtenidas
        if failures:
            resultados[f"{nombre}_failed"] = failures

        if save and obtenidas:
            try:
                if nombre == 'contraseña' and hasattr(palabras_generadas_db, 'insertar_contrasenas_batch'):
                    palabras_generadas_db.insertar_contrasenas_batch(obtenidas)
                elif nombre == 'correo' and hasattr(palabras_generadas_db, 'insertar_correos_batch'):
                    palabras_generadas_db.insertar_correos_batch(obtenidas)
                elif nombre == 'direccion' and hasattr(palabras_generadas_db, 'insertar_direcciones_batch'):
                    palabras_generadas_db.insertar_direcciones_batch(obtenidas)
                elif nombre == 'telefono' and hasattr(palabras_generadas_db, 'insertar_telefonos_batch'):
                    palabras_generadas_db.insertar_telefonos_batch(obtenidas)
                elif nombre == 'usuario' and hasattr(palabras_generadas_db, 'insertar_usuarios_batch'):
                    palabras_generadas_db.insertar_usuarios_batch(obtenidas)
                else:
                    if nombre == 'contraseña':
                        for v in obtenidas:
                            palabras_generadas_db.insertar_contrasena(v)
                    elif nombre == 'correo':
                        for v in obtenidas:
                            palabras_generadas_db.insertar_correo(v)
                    elif nombre == 'direccion':
                        for v in obtenidas:
                            palabras_generadas_db.insertar_direccion(v)
                    elif nombre == 'telefono':
                        for v in obtenidas:
                            palabras_generadas_db.insertar_telefono(v)
                    elif nombre == 'usuario':
                        for v in obtenidas:
                            palabras_generadas_db.insertar_usuario(v)
                    else:
                        pass
            except Exception:
                for v in obtenidas:
                    try:
                        if nombre == 'contraseña':
                            palabras_generadas_db.insertar_contrasena(v)
                        elif nombre == 'correo':
                            palabras_generadas_db.insertar_correo(v)
                        elif nombre == 'direccion':
                            palabras_generadas_db.insertar_direccion(v)
                        elif nombre == 'telefono':
                            palabras_generadas_db.insertar_telefono(v)
                        elif nombre == 'usuario':
                            palabras_generadas_db.insertar_usuario(v)
                    except Exception:
                        continue

    return resultados


if __name__ == "__main__":
    for nombre in ['contraseña', 'correo', 'direccion', 'telefono', 'usuario']:
        try:
            ejemplos = generar_varias(nombre, 5, max_tokens=20)
        except Exception as e:
            ejemplos = [f"ERROR: {e}"]
        print(f"== {nombre} ==")
        for e in ejemplos:
            print(e)
        print()
