from typing import List

from fastapi import APIRouter, status, Body

from app.schemas.command_schemas import CommandRequestSchema, CommandResponseSchema, CommandTypeResponseSchema
from app.services.command_service import CommandService

commands_router = APIRouter(
    prefix="/commands",
    tags=["Commands"]
)

@commands_router.get(
    "/available-types",
    response_model=List[CommandTypeResponseSchema]
)
async def get_command_types() -> List[CommandTypeResponseSchema]:
    """
    Retrieves all available command types that can be issued to equipment.
    \f
    :return: List of all available command types.
    """
    return await CommandService.get_command_types()


@commands_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CommandResponseSchema,
    summary="Send command to equipment",
    description="Sends a command to an equipment via MQTT. "
                "Requires equipment_id, command_type_id, and optional payload."
)
async def post_command(
        command_data: CommandRequestSchema = Body(..., description="Data information of the command solicitation"),
) -> CommandResponseSchema:
    """
    Post a command to equipment.
    \f
    :param command_data: Data information of the command solicitation.
    """
    return await CommandService.post_command(command_data)


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
