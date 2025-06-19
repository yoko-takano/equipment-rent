from fastapi import APIRouter
from starlette import status

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post(
    "",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Asset Administration Shell created successfully"},
        400: {"description": "Bad Request, e.g. the request parameters of the format of the request body is wrong"},
        401: {"description": "Unauthorized, e.g. the server refused the authorization attempt"}
    },
    summary="Creates a new Asset Administration Shell",
)
async def post_asset_administration_shell(
        aas_payload: str,
) -> str:
    """
    Creates a new Asset Administration Shell.
    The id of the new Asset Administration Shell must be set in the payload.
    \f
    :param aas_payload: Asset Administration Shell object.
    :return: Created Asset Administration Shell.
    """
    return "ok"
