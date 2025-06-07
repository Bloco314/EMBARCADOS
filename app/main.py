from fastapi import FastAPI
from .routes import router as routes_router
from .mqtt_service import start_mqtt
from .dbservice import create_tables

app = FastAPI()

app.include_router(routes_router)
create_tables()
start_mqtt()
