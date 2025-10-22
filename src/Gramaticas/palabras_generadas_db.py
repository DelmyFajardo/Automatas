
import sqlite3
import os
from typing import Optional

MODULE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(MODULE_DIR, 'palabras_generadas.db')


def crear_tablas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contrasenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contrasena TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS correos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS direcciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direccion TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telefonos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def insertar_contrasena(contrasena: str):
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contrasenas (contrasena) VALUES (?)', (contrasena,))
    conn.commit()
    conn.close()

def insertar_correo(correo: str):
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO correos (correo) VALUES (?)', (correo,))
    conn.commit()
    conn.close()

def insertar_direccion(direccion: str):
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO direcciones (direccion) VALUES (?)', (direccion,))
    conn.commit()
    conn.close()

def insertar_telefono(telefono: str):
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO telefonos (telefono) VALUES (?)', (telefono,))
    conn.commit()
    conn.close()

def insertar_usuario(usuario: str):
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (usuario) VALUES (?)', (usuario,))
    conn.commit()
    conn.close()


def insertar_contrasenas_batch(contrasenas: list):
    if not contrasenas:
        return
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO contrasenas (contrasena) VALUES (?)', ((c,) for c in contrasenas))
    conn.commit()
    conn.close()


def insertar_correos_batch(correos: list):
    if not correos:
        return
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO correos (correo) VALUES (?)', ((c,) for c in correos))
    conn.commit()
    conn.close()


def insertar_direcciones_batch(direcciones: list):
    if not direcciones:
        return
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO direcciones (direccion) VALUES (?)', ((d,) for d in direcciones))
    conn.commit()
    conn.close()


def insertar_telefonos_batch(telefonos: list):
    if not telefonos:
        return
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO telefonos (telefono) VALUES (?)', ((t,) for t in telefonos))
    conn.commit()
    conn.close()


def insertar_usuarios_batch(usuarios: list):
    if not usuarios:
        return
    crear_tablas()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO usuarios (usuario) VALUES (?)', ((u,) for u in usuarios))
    conn.commit()
    conn.close()


def obtener_contrasenas():
    return obtener_generico('contrasenas')

def obtener_correos():
    return obtener_generico('correos')

def obtener_direcciones():
    return obtener_generico('direcciones')

def obtener_telefonos():
    return obtener_generico('telefonos')

def obtener_usuarios():
    return obtener_generico('usuarios')


def obtener_generico(tabla: str, column: str | None = None, limit: int | None = None):
   
    if column is None:
        mapping = {
            'contrasenas': 'contrasena',
            'correos': 'correo',
            'direcciones': 'direccion',
            'telefonos': 'telefono',
            'usuarios': 'usuario'
        }
        column = mapping.get(tabla, None)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if limit is None:
        cursor.execute(f'SELECT {column} FROM {tabla} ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]
    else:
        cursor.execute(f'SELECT {column} FROM {tabla} ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in reversed(rows)]
