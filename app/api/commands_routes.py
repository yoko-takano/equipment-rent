from fastapi import APIRouter, status

commands_router = APIRouter(
    prefix="/commands",
    tags=["Commands"]
)

@commands_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Send command to equipment",
    description="Sends a command to an equipment via MQTT. "
                "Requires equipment_id, command_type_id, and optional payload."
)
async def send_command(command_data: dict):
    """
    Sends a command to equipment.
    """
    return f"command sent {command_data}"


@commands_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all commands",
    description="Returns all commands sent."
)
async def list_commands():
    """
    Lists all commands.
    """
    return "list commands"


@commands_router.get(
    "/{command_id}",
    status_code=status.HTTP_200_OK,
    summary="Get command details",
    description="Returns details of a specific command."
)
async def get_command(command_id: str):
    """
    Retrieves details of the specified command.
    """
    return f"get command {command_id}"
