from abc import ABC, abstractmethod
from typing import List

from app.schemas.command_schemas import CommandRequestSchema, CommandResponseSchema, CommandTypeResponseSchema


class ICommandService(ABC):
    """
    Interface class responsible for command-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_command_types(cls) -> List[CommandTypeResponseSchema]:
        """
        Retrieves all available command types.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def post_command(
            cls,
            command_data: CommandRequestSchema,
    ) -> CommandResponseSchema:
        """
        Validates the existence of the equipment and create/post command.
        """
        raise NotImplementedError
