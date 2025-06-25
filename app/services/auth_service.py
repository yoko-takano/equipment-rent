from datetime import timedelta, timezone, datetime
from typing import Type

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from starlette import status

from app.core.config import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_scheme
from app.database import UserAuth, User
from app.interface.auth_interface import IAuthService
from app.schemas.user_auth_schemas import UserRequestSchema, UserResponseSchema, TokenSchema
from tools.application import Service


class AuthService(Service):
    """
    Service class responsible for authentication-related operations.
    """
    def __new__(
        cls,
        auth_service:Type[IAuthService],
    ):
        cls.auth_service = auth_service
        return cls

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Hashes a plaintext password.
        """
        return pwd_context.hash(password)

    @classmethod
    async def post_user(
            cls,
            user_info: UserRequestSchema
    ) -> UserResponseSchema:
        """
        Registers a new user with the given credentials.
        """
        existing_auth = await UserAuth.filter(username=user_info.username).first()

        if existing_auth:
            raise HTTPException(status_code=400, detail="Username already registered")

        create_user = await User.create(
            name=user_info.name,
            email=user_info.email
        )

        hashed_password = cls.get_password_hash(user_info.password)

        create_user_auth = await UserAuth.create(
            username=user_info.username,
            password_hash=hashed_password,
            user=create_user
        )

        user_response = UserResponseSchema(
            id=create_user_auth.id,
            name=create_user.name,
            username=create_user_auth.username,
            email=create_user.email,
            is_active=create_user.is_active
        )

        return user_response

    @classmethod
    async def login_user(
            cls,
            form_data: OAuth2PasswordRequestForm
    ) -> TokenSchema:
        """
        Authenticates the user and returns a JWT access token.
        """
        user_auth = await UserAuth.get_or_none(username=form_data.username).prefetch_related("user")

        if not user_auth or not pwd_context.verify(form_data.password, user_auth.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + access_token_expires
        to_encode = {
            "sub": user_auth.username,
            "exp": expire
        }
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return TokenSchema(access_token=access_token, token_type="bearer")

    @classmethod
    async def get_current_active_user(
            cls,
            token: str = Depends(oauth2_scheme)
    ) -> UserResponseSchema:
        """
        Extracts the user from the JWT token and ensures they are active.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except (ExpiredSignatureError, InvalidTokenError):
            raise credentials_exception

        user_auth = await UserAuth.get_or_none(username=username).prefetch_related("user")
        if not user_auth or not user_auth.user.is_active:
            raise credentials_exception

        return UserResponseSchema(
            id=user_auth.id,
            name=user_auth.user.name,
            username=user_auth.username,
            email=user_auth.user.email,
            is_active=user_auth.user.is_active
        )
