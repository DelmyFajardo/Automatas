import sqlite3
import json
from typing import Dict, Optional
from palabras_generadas_db import DB_PATH


def crear_tabla_gramaticas() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS gramaticas (
            nombre TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def insertar_gramatica(nombre: str, gr: Dict) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    payload = json.dumps(gr, ensure_ascii=False)
    cur.execute('INSERT OR REPLACE INTO gramaticas (nombre, data) VALUES (?, ?)', (nombre, payload))
    conn.commit()
    conn.close()


def obtener_gramatica(nombre: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT data FROM gramaticas WHERE nombre = ?', (nombre,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row[0])


def obtener_todas_gramaticas() -> Dict[str, Dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT nombre, data FROM gramaticas')
    rows = cur.fetchall()
    conn.close()
    return {nombre: json.loads(data) for nombre, data in rows}


def eliminar_gramatica(nombre: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DELETE FROM gramaticas WHERE nombre = ?', (nombre,))
    conn.commit()
    conn.close()
