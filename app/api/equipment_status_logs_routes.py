from fastapi import APIRouter, status


equipment_status_logs_router = APIRouter(
    prefix="/equipment-status-logs",
    tags=["EquipmentStatusLogs"]
)

@equipment_status_logs_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all equipment status logs",
    description="Returns all equipment status logs."
)
async def list_equipment_status_logs():
    """
    Lists all equipment status logs.
    """
    return "list equipment status logs"


@equipment_status_logs_router.get(
    "/{equipment_id}",
    status_code=status.HTTP_200_OK,
    summary="Get status logs for a specific equipment",
    description="Returns status logs for the specified equipment."
)
async def get_status_logs_for_equipment(equipment_id: str):
    """
    Retrieves status logs for a specific equipment.
    """
    return f"status logs for equipment {equipment_id}"
