import asyncio
from tortoise import Tortoise
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
import uuid
from gmqtt import Client as MQTTClient

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "rent-mosquitto")
print(MQTT_BROKER_HOST)
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "equipment-rent-api")

mqtt = MQTTClient(MQTT_CLIENT_ID)


@mqtt.on_connect
def on_connect(client, flags, rc, properties):
    print("[MQTT] Connected")
    client.subscribe("equipments/+/status")
    client.subscribe("equipments/+/feedback")

async def handle_status_message(topic: str, payload: bytes):
    print(f"Status: {topic} -> {payload.decode()}")

async def handle_feedback_message(topic: str, payload: bytes):
    print(f"Feedback: {topic} -> {payload.decode()}")

@mqtt.on_message
async def on_message(client, topic, payload, qos, properties):
    print(f"[MQTT] Message received - Topic: {topic}")
    if "status" in topic:
        await handle_status_message(topic, payload)
    elif "feedback" in topic:
        await handle_feedback_message(topic, payload)


async def connect_mqtt(retries=5, delay=2):
    for attempt in range(retries):
        try:
            await mqtt.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
            print(f"[MQTT] Connected to {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
            return
        except Exception as e:
            print('erro: ', e)
            if attempt == retries - 1:
                raise
            print(f"[MQTT] Connection attempt: {MQTT_BROKER_HOST} {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)

def publish_command(equipment_id: uuid.UUID, command: str):
    topic = f"equipments/{equipment_id}/commands"
    mqtt.publish(topic, command)

# Database Configuration
async def init_db(app: FastAPI, retries=10, delay=3):
    db_url = "postgres://rentdb:rentdb@rent-postgres:5432/rent"
    for attempt in range(retries):
        try:
            await Tortoise.init(
                db_url=db_url,
                modules={"models": ["app.database"]},
            )
            await Tortoise.generate_schemas(safe=True)
            print("Database connected!")
            return
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("Could not connect to the database after multiple retries")

# JWT Configuration
SECRET_KEY = "ffc2c1bf196a3a3ebbfcf731f4b03fe57239c2e81be50bd23a36e472ef3913b2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
