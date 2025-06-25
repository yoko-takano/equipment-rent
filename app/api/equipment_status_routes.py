from fastapi import APIRouter, status

from app.services.equipment_service import EquipmentService

equipment_status_router = APIRouter(
    prefix="/equipment-status",
    tags=["EquipmentStatus"]
)

@equipment_status_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all possible equipment statuses",
    description="Returns all possible statuses that equipment can have."
)
async def get_equipment_status():
    """
    Lists all equipment statuses.
    """
    return await EquipmentService.get_equipment_status()
