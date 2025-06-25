from abc import ABC, abstractmethod

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import oauth2_scheme
from app.schemas.user_auth_schemas import UserResponseSchema, UserRequestSchema, TokenSchema


class IAuthService(ABC):
    """
    Interface class responsible for authentication-related operations.
    """
    @classmethod
    @abstractmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Hashes a plaintext password.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def post_user(
            cls,
            user_info: UserRequestSchema
    ) -> UserResponseSchema:
        """
        Registers a new user with the given credentials.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def login_user(
            cls,
            form_data: OAuth2PasswordRequestForm
    ) -> TokenSchema:
        """
        Authenticates the user and returns a JWT access token.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_current_active_user(
            cls,
            token: str = Depends(oauth2_scheme)
    ) -> UserResponseSchema:
        """
        Extracts the user from the JWT token and ensures they are active.
        """
        raise NotImplementedError()

