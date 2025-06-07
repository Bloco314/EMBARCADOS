import sqlite3
from datetime import datetime
from typing import Optional

DB_NAME = "embarcados.db"


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
