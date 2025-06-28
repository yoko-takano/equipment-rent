import asyncio
from typing import List
from uuid import UUID

from app.core.config import mqtt
from app.database import CommandType, Command
from app.interfaces.command_interface import ICommandService
from app.mqqt_client.mqtt_service import publish_command, publish_status
from app.schemas.command_schemas import CommandTypeResponseSchema, CommandRequestSchema, CommandResponseSchema, \
    CommandTypeEnum, CommandPayloadSchema


class CommandPersistence(ICommandService):
    """
    Persistence class responsible for authentication-related operations.
    """
    @classmethod
    async def get_command_types(cls) -> List[CommandTypeResponseSchema]:
        """
        Retrieves all available command types.
        """
        command_types = await CommandType.all()
        commands_list: List[CommandTypeResponseSchema] = []

        for command in command_types:
            command_response = CommandTypeResponseSchema(
                id=command.id,
                name=command.name,
                created_at=command.created_at,
            )
            commands_list.append(command_response)

        return commands_list

    @classmethod
    async def post_command(
            cls,
            command_data: CommandRequestSchema,
    ) -> CommandResponseSchema:
        """
        Creates a new command record in the database and publishes it to the corresponding MQTT topic.
        """
        # Save command to database
        command = await Command.create(
            equipment_id=command_data.equipment_id,
            command_type_id=command_data.command_type_id,
            payload=command_data.payload
        )

        # Retrieves the command name type
        command_type = await CommandType.get(id=command_data.command_type_id)

        # Define payload for publish
        command_payload = CommandPayloadSchema(
            command_type=command_type.name,
            payload=command_data.payload
        )

        # Publish command to MQTT using helper
        publish_command(command_data.equipment_id, command_payload.model_dump())

        # Return response schema
        return CommandResponseSchema(
            id=command.id,
            equipment_id=command.equipment_id,
            command_type_id=command.command_type_id,
            payload=command.payload,
            created_at=command.created_at
        )
