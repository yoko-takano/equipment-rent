from app.database import EquipmentStatus
from app.schemas.equipment_schemas import EquipmentStatusEnum


async def seed_equipment_statuses():
    for status in EquipmentStatusEnum:
        await EquipmentStatus.get_or_create(name=status.value)
