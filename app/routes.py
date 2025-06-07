from fastapi import APIRouter, Body, Query
from typing import Optional
from .mqtt_service import publish_message
from .list_utils_json import *
from .dbservice import mock_data

router = APIRouter()


@router.post("/mqtt/publish")
async def mqtt_publish(topic: str, message: str):
    publish_message(topic, message)
    return {"status": "mensagem enviada", "topico": topic, "mensagem": message}


@router.post("/mqtt/publish-json")
async def mqtt_publish_json(topic: str, data: dict = Body(...)):
    publish_message(topic, data)
    return {"status": "mensagem JSON enviada", "topico": topic, "dados": data}

@router.post("/mock-data")
async def fill_data():
    mock_data()
    return {"status": "banco preenchido"}

@router.get("/list-all/reads")
async def get_leituras():
    return listar_leituras()


@router.get("/list-all/logs")
async def get_logs():
    return listar_logs()


@router.get("/list/reads-filtered")
async def get_leituras_intervalo(
    inicio: Optional[str] = Query(None, description="Timestamp inicial (ISO format)"),
    fim: Optional[str] = Query(None, description="Timestamp final (ISO format)"),
):
    return listar_leituras_por_intervalo(inicio, fim)


@router.get("/list/logs-filtered")
async def get_logs_intervalo(
    inicio: Optional[str] = Query(None, description="Timestamp inicial (ISO format)"),
    fim: Optional[str] = Query(None, description="Timestamp final (ISO format)"),
):
    return listar_logs_por_intervalo(inicio, fim)


@router.get("/get/last-read")
async def get_last_read():
    return query_last_read()


@router.get("/get/n-last-logs")
async def get_last_logs(n: int):
    return query_n_last_logs(n)
