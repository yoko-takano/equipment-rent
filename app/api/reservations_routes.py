from fastapi import APIRouter, status

reservations_router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@reservations_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new reservation",
    description="Creates a new equipment reservation. Requires user_id, equipment_id, start_time, end_time."
)
async def create_reservation(reservation_data: dict):
    """
    Creates a new reservation.
    """
    return "create reservation"


@reservations_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all reservations",
    description="Returns a list of all reservations."
)
async def list_reservations():
    """
    Lists all reservations.
    """
    return "list reservations"


@reservations_router.get(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    summary="Get reservation details",
    description="Returns details of a specific reservation by reservation_id."
)
async def get_reservation(reservation_id: str):
    """
    Retrieves details of the specified reservation.
    """
    return f"get reservation {reservation_id}"


@reservations_router.patch(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK,
    summary="Update reservation status",
    description="Updates the status of a reservation."
)
async def update_reservation(reservation_id: str, update_data: dict):
    """
    Updates the status of the specified reservation.
    """
    return f"update reservation {reservation_id}"


@reservations_router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel reservation",
    description="Cancels a reservation."
)
async def cancel_reservation(reservation_id: str):
    """
    Cancels the specified reservation.
    """
    return
