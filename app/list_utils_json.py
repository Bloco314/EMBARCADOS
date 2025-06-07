import sqlite3
from datetime import datetime
from typing import Optional
import os

DB_NAME = os.path.join(os.getenv("DB_PATH", "."), "embarcados.db")


def listar_leituras():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM leituras")
    resultados = cursor.fetchall()
    conn.close()

    leituras_formatadas = []
    for row in resultados:
        leitura = {
            "id": row[0],
            "id_zona": row[1],
            "timestamp": datetime.fromisoformat(row[2]).strftime("%Y-%m-%d %H:%M"),
            "umidade": row[3],
            "temperatura": row[4],
        }
        leituras_formatadas.append(leitura)

    return leituras_formatadas


def listar_leituras_por_intervalo(
    inicio: Optional[str] = None, fim: Optional[str] = None
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT rowid, * FROM leituras"
    params = []

    if inicio and fim:
        query += " WHERE timestamp BETWEEN ? AND ?"
        params.extend([inicio, fim])
    elif inicio:
        query += " WHERE timestamp >= ?"
        params.append(inicio)
    elif fim:
        query += " WHERE timestamp <= ?"
        params.append(fim)

    query += " ORDER BY timestamp ASC"
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()

    leituras_formatadas = []
    for row in resultados:
        leitura = {
            "id": row[0],
            "id_zona": row[1],
            "timestamp": datetime.fromisoformat(row[2]).strftime("%Y-%m-%d %H:%M"),
            "umidade": row[3],
            "temperatura": row[4],
        }
        leituras_formatadas.append(leitura)

    return leituras_formatadas


def listar_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM log_acoes")
    resultados = cursor.fetchall()
    conn.close()

    logs_formatados = []
    for row in resultados:
        log = {
            "id": row[0],
            "id_zona": row[2],
            "timestamp": datetime.fromisoformat(row[3]).strftime("%Y-%m-%d %H:%M"),
            "action": row[4],
            "manual": bool(row[5]),
        }
        logs_formatados.append(log)

    return logs_formatados


def listar_logs_por_intervalo(inicio: Optional[str] = None, fim: Optional[str] = None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT rowid, * FROM log_acoes"
    params = []

    if inicio and fim:
        query += " WHERE timestamp BETWEEN ? AND ?"
        params.extend([inicio, fim])
    elif inicio:
        query += " WHERE timestamp >= ?"
        params.append(inicio)
    elif fim:
        query += " WHERE timestamp <= ?"
        params.append(fim)

    query += " ORDER BY timestamp ASC"
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()

    logs_formatados = []
    for row in resultados:
        log = {
            "id": row[0],
            "id_zona": row[2],
            "timestamp": datetime.fromisoformat(row[3]).strftime("%Y-%m-%d %H:%M"),
            "action": row[4],
            "manual": bool(row[5]),
        }
        logs_formatados.append(log)

    return logs_formatados


def query_last_read():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT rowid, * FROM leituras
        ORDER BY timestamp DESC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"msg": "nenhuma leitura encontrada"}

    leitura = {
        "id": row[0],
        "id_zona": row[1],
        "timestamp": datetime.fromisoformat(row[2]).strftime("%Y-%m-%d %H:%M"),
        "umidade": row[3],
        "temperatura": row[4],
    }

    return leitura


def query_n_last_logs(n: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT rowid, * FROM log_acoes
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (n,),
    )

    resultados = cursor.fetchall()
    conn.close()

    logs_formatados = []
    for row in resultados:
        log = {
            "id": row[0],
            "id_zona": row[2],
            "timestamp": datetime.fromisoformat(row[3]).strftime("%Y-%m-%d %H:%M"),
            "action": row[4],
            "manual": bool(row[5]),
        }
        logs_formatados.append(log)

    return logs_formatados
