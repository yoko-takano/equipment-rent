from typing import List
from uuid import UUID

from app.interface.user_interface import IUserService
from app.schemas.user_auth_schemas import UserUpdateSchema, UserResponseSchema


class UserPersistence(IUserService):
    """
    Persistence class for user-related operations.
    """
    @classmethod
    async def get_users(cls) -> List[UserResponseSchema]:
        """
        Retrieves a list of all registered users along with their authentication details.
        """
        pass

    @classmethod
    async def get_specific_user(cls, user_id: UUID) -> UserResponseSchema:
        """
        Retrieves a specific user by their ID, including authentication and profile details.
        """
        pass

    @classmethod
    async def patch_user(cls, user_id: UUID, user_data: UserUpdateSchema) -> UserResponseSchema:
        """
        Updates user information such as name, username and email.
        """
        pass

    @classmethod
    async def delete_user(cls, user_id: UUID):
        """
        Deactivates a user by setting is_active to False.
        """
        pass
