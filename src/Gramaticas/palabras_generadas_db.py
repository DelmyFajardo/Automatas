
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


def obtener_contrasenas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT contrasena FROM contrasenas')
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]

def obtener_correos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT correo FROM correos')
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]

def obtener_direcciones():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT direccion FROM direcciones')
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]

def obtener_telefonos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT telefono FROM telefonos')
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]

def obtener_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT usuario FROM usuarios')
    resultados = cursor.fetchall()
    conn.close()
    return [fila[0] for fila in resultados]
