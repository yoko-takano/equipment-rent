"""Configures the api server."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth_routes import auth_router
from app.api.commands_routes import commands_router
from app.api.equipment_status_routes import equipment_status_router
from app.api.equipment_status_logs_routes import equipment_status_logs_router
from app.api.equipments_routes import equipments_router
from app.api.reservations_routes import reservations_router
from app.api.users_routes import users_router
from app.core.config import init_db, connect_mqtt
from app.core.dependencies import inject_dependencies
from app.core.seeds import seed_equipment_statuses, seed_reservation_statuses, seed_command_types
import app.mqqt_client.mqtt_service

tags_metadata = [
    {
        "name": "Auth",
        "description": "Handles user registration, login, and access to authenticated user information using JWT "
                       "tokens."
    },
    {
        "name": "Users",
        "description": "Manages system users, allowing listing, retrieval, updates, and deletion of user accounts."
    },
    {
        "name": "Equipments",
        "description": "Provides access to equipment data, including listing, creation, updates, deletion, and status "
                       "retrieval."
    },
    {
        "name": "Reservations",
        "description": "Manages equipment reservations, including creation, listing, updating reservation status, and "
                       "cancellation."
    },
    {
        "name": "Commands",
        "description": "Sends and retrieves commands sent to equipment via MQTT, including command details and payload."
    },
    {
        "name": "EquipmentStatus",
        "description": "Provides all possible equipment statuses and logs of equipment status changes, including "
                       "filtering by equipment."
    }
]

# Initializes the Tortoise ORM database connection and creates tables if needed
@asynccontextmanager
async def lifespan(application: FastAPI):
    await init_db(application)
    await connect_mqtt()
    await seed_equipment_statuses()
    await seed_reservation_statuses()
    await seed_command_types()
    inject_dependencies()
    yield

app = FastAPI(
    title="Equipment Reservation and Control API",
    version="1.0.0",
    lifespan=lifespan,
    description=(
        "This API provides endpoints for managing equipment reservations and sending remote control commands. "
        "It enables users to interact with devices in real time through a secure and efficient interface. "
        "Authentication is handled via JWT, and device communication is established through MQTT messaging."
    ),
    openapi_tags=tags_metadata,
    terms_of_service="/terms",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register the API routes to the FastAPI application
app.include_router(users_router)
app.include_router(equipments_router)
app.include_router(equipment_status_logs_router)
app.include_router(equipment_status_router)
app.include_router(auth_router)
app.include_router(reservations_router)
app.include_router(commands_router)
