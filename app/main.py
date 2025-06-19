"""Configures the api server."""
from fastapi import FastAPI, Request
from app.api.users import users_router
from app.core.config import init_db

tags_metadata = [
    {
        "name": "UserAuth",
        "description": "Handles user registration, login, and access to authenticated user information using JWT tokens."
    },
    {
        "name": "Users",
        "description": "Manages system users, allowing listing, retrieval, updates, and deletion of user accounts."
    },
    {
        "name": "Equipments",
        "description": "Provides access to equipment data, including listing, creation, updates, deletion, and status retrieval."
    },
    {
        "name": "Reservations",
        "description": "Manages equipment reservations, including creation, listing, updating reservation status, and cancellation."
    },
    {
        "name": "Commands",
        "description": "Sends and retrieves commands sent to equipment via MQTT, including command details and payload."
    },
    {
        "name": "EquipmentStatuses",
        "description": "Defines all possible statuses that equipment can assume in the system."
    },
    {
        "name": "EquipmentStatus",
        "description": "Provides all possible equipment statuses and logs of equipment status changes, including filtering by equipment."
    }
]

app = FastAPI(
    title="Equipment Reservation and Control API",
    version="1.0.0",
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

# Initializes the Tortoise ORM database connection and creates tables if needed
init_db(app)

# Register the API routes to the FastAPI application
app.include_router(users_router)
