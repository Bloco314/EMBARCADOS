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
        timestamp TEXT,
        umidade REAL,
        temperatura REAL,
        PRIMARY KEY (ID_ZONA, timestamp)
    )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS log_acoes (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_ZONA INTEGER,
            timestamp TEXT,
            log VARCHAR(50),
            Manual BOOLEAN
        )
        """
    )

    conn.commit()
    conn.close()


def salvar_leitura(id_zona: int, umidade: float, temperatura: float):
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO leituras (ID_ZONA, timestamp, umidade, temperatura)
        VALUES (?, ?, ?, ?)
    """,
        (id_zona, timestamp, umidade, temperatura),
    )

    conn.commit()
    conn.close()


def salvar_log_acao(id_zona: int, log: str, manual: bool):
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO log_acoes (ID_ZONA, timestamp, log, manual)
        VALUES (?, ?, ?, ?)
    """,
        (id_zona, timestamp, log, int(manual)),
    )
    conn.commit()
    conn.close()


def mock_data():
    temperaturas = [i * 10 for i in range(1, 10)]
    umidades = [30, 60, 90]
    for id_zona in range(1, 11):
        for u in umidades:
            for t in temperaturas:
                salvar_leitura(id_zona, u, t)
