import sqlite3
from datetime import datetime
from typing import Optional

DB_NAME = "embarcados.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS leituras (
        ID_ZONA INTEGER,
        Timestamp TEXT,
        Umidade REAL,
        PH REAL,
        PRIMARY KEY (ID_Zona, Timestamp)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS log_acoes (
        Timestamp TEXT PRIMARY KEY,
        Acao VARCHAR(50),
        Manual BOOLEAN
    )
    """
    )

    conn.commit()
    conn.close()


def salvar_leitura(id_zona: int, umidade: float, ph: float):
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO leituras (ID_Zona, Timestamp, Umidade, PH)
        VALUES (?, ?, ?, ?)
    """,
        (id_zona, timestamp, umidade, ph),
    )

    conn.commit()
    conn.close()


def salvar_log_acao(acao: str, manual: bool):
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO log_acoes (Timestamp, Acao, Manual)
        VALUES (?, ?, ?)
    """,
        (timestamp, acao, int(manual)),
    )
    conn.commit()
    conn.close()


def listar_leituras():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leituras")
    resultados = cursor.fetchall()

    conn.close()
    return resultados


def listar_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM log_acoes")
    resultados = cursor.fetchall()

    conn.close()
    return resultados


def listar_leituras_por_intervalo(
    inicio: Optional[str] = None, fim: Optional[str] = None
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT * FROM leituras"
    params = []

    if inicio and fim:
        query += " WHERE Timestamp BETWEEN ? AND ?"
        params.extend([inicio, fim])
    elif inicio:
        query += " WHERE Timestamp >= ?"
        params.append(inicio)
    elif fim:
        query += " WHERE Timestamp <= ?"
        params.append(fim)

    query += " ORDER BY Timestamp ASC"

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def listar_logs_por_intervalo(inicio: Optional[str] = None, fim: Optional[str] = None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT * FROM log_acoes"
    params = []

    if inicio and fim:
        query += " WHERE Timestamp BETWEEN ? AND ?"
        params.extend([inicio, fim])
    elif inicio:
        query += " WHERE Timestamp >= ?"
        params.append(inicio)
    elif fim:
        query += " WHERE Timestamp <= ?"
        params.append(fim)

    query += " ORDER BY Timestamp ASC"

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def listar_leituras_json():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM leituras")
    resultados = cursor.fetchall()

    conn.close()

    leituras_formatadas = []
    for row in resultados:
        leitura = {
            "id": row[0],
            "timestamp": datetime.fromisoformat(row[2]).strftime('%Y-%m-%d %H:%M'),
            "ph": row[3],
            "humidity": row[4]
        }
        leituras_formatadas.append(leitura)

    return leituras_formatadas