from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as routes_router
from .mqtt_service import start_mqtt
from .dbservice import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique os domínios, ex: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # ou especifique: ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)

app.include_router(routes_router)
create_tables()
start_mqtt()
