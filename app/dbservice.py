import sqlite3
from datetime import datetime
import os

DB_NAME = os.path.join(os.getenv("DB_PATH", "."), "embarcados.db")


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
