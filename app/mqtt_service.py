import paho.mqtt.client as mqtt
import json
from .dbservice import salvar_leitura, salvar_log_acao

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
PREFIX = "bhive"

# Topicos a serem observados
MQTT_TOPICS = ["data"]


def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Conectado com código: {rc}")
    client.subscribe(PREFIX + "/" + MQTT_TOPICS[0])


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        if msg.topic.startswith(PREFIX + "/" + MQTT_TOPICS[0]):
            print(f"[MQTT] {msg.topic} => {payload}")
            zona = payload.get("zona")
            humidity = payload.get("humidity")
            ph = payload.get("ph")
            salvar_leitura(zona, humidity, ph)

    except json.JSONDecodeError:
        print("Erro ao decodificar a mensagem")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def start_mqtt():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    mqtt_client.loop_start()


def publish_message(topic: str, message: str):
    mqtt_client.publish(topic, message)


def publish_message(topic: str, data: dict):
    try:
        payload = json.dumps(data)
        mqtt_client.publish(topic, payload)
    except (TypeError, ValueError) as e:
        print(f"Erro ao converter dados para JSON: {e}")
