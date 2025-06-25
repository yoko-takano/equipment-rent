from typing import List, Type
from uuid import UUID

from fastapi import HTTPException
from starlette import status

from app.database import UserAuth
from app.interface.user_interface import IUserService
from app.schemas.user_auth_schemas import UserResponseSchema, UserUpdateSchema
from tools.application import Service


class UserService(Service):
    """
    Service class for user-related operations.
    """
    def __new__(
        cls,
        user_service:Type[IUserService],
    ):
        cls.user_service = user_service
        return cls

    @classmethod
    async def get_users(cls) -> List[UserResponseSchema]:
        """
        Retrieves a list of all registered users along with their authentication details.
        """
        auth_records = await UserAuth.all().prefetch_related("user")
        user_list: List[UserResponseSchema] = []

        for auth in auth_records:
            user = auth.user
            user_response = UserResponseSchema(
                id=auth.id,
                username=auth.username,
                name=user.name,
                email=user.email,
                is_active=user.is_active
            )

            user_list.append(user_response)

        return user_list

    @classmethod
    async def get_specific_user(cls, user_id: UUID) -> UserResponseSchema:
        """
        Retrieves a specific user by their ID, including authentication and profile details.
        """
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")

        if not user_auth:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_response = UserResponseSchema(
            id=user_auth.id,
            username=user_auth.username,
            name=user_auth.user.name,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )

        return user_response

    @classmethod
    async def patch_user(cls, user_id: UUID, user_data: UserUpdateSchema) -> UserResponseSchema:
        """
        Updates user information such as name, username and email.
        """
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")
        if not user_auth:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_data.name is not None:
            user_auth.user.name = user_data.name
        if user_data.email is not None:
            user_auth.user.email = user_data.email

        if user_data.username is not None:
            existing = await UserAuth.get_or_none(username=user_data.username)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Username already taken")
            user_auth.username = user_data.username

        await user_auth.user.save()
        await user_auth.save()

        return UserResponseSchema(
            id=user_auth.id,
            username=user_auth.username,
            name=user_auth.user.name,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )

    @classmethod
    async def delete_user(cls, user_id: UUID):
        """
        Deactivates a user by setting is_active to False.
        """
        user_auth = await UserAuth.get_or_none(id=user_id).prefetch_related("user")

        if not user_auth:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_auth.user.is_active = False
        await user_auth.user.save()
