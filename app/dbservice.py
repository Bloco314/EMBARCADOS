import sqlite3
from datetime import datetime, timedelta
import os
import random

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


def salvar_leitura(id_zona: int, umidade: float, temperatura: float, timestamp: str = None):
    if timestamp is None:
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
    temperaturas = [i * 5 for i in range(4, 10)]
    umidades = [30, 50, 70, 90]
    start_date = datetime(2025, 1, 1)

    for id_zona in range(1, 11):
        for month_offset in range(0, 6):
            base_date = start_date + timedelta(days=30 * month_offset)
            for day in range(1, 28, 7):
                temp = random.choice(temperaturas)
                umid = random.choice(umidades)
                
                date = base_date.replace(day=day)
                time_offset = timedelta(hours=random.choice([8, 15]))
                full_timestamp = (date + time_offset).isoformat()
                salvar_leitura(id_zona, umid, temp, timestamp=full_timestamp)
