from typing import Type, List

from fastapi import HTTPException
from starlette import status

from app.database import Equipment, EquipmentStatus
from app.interface.equipment_interface import IEquipmentService
from app.schemas.equipment_schemas import EquipmentStatusEnum, EquipmentResponseSchema, \
    EquipmentRequestSchema, EquipmentStatusResponseSchema


class EquipmentService:
    """
    Service class responsible for equipment-related operations.
    """
    def __new__(
        cls,
        equipment_service:Type[IEquipmentService],
    ):
        cls.equipment_service = equipment_service
        return cls

    @classmethod
    async def get_equipment_status(cls) -> List[EquipmentStatusResponseSchema]:
        """
        Retrieves all possible equipment statuses.
        """
        status_record = await EquipmentStatus.all()
        status_list: List[EquipmentStatusResponseSchema] = []

        for equipment_status in status_record:
            status_response = EquipmentStatusResponseSchema(
                id=equipment_status.id,
                name=equipment_status.name,
                created_at=equipment_status.created_at,
            )
            status_list.append(status_response)

        return status_list

    @classmethod
    async def get_equipments(cls):
        """

        """
        pass

    @classmethod
    async def post_equipment(
            cls,
            equipment_data: EquipmentRequestSchema,
    ) -> EquipmentResponseSchema:

        existing = await Equipment.get_or_none(name=equipment_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Equipment with this name already exists"
            )

        status_exists = await EquipmentStatus.get_or_none(id=equipment_data.current_status_id)
        if not status_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipment status not found"
            )

        equipment = await Equipment.create(
            name=equipment_data.name,
            current_status_id=equipment_data.current_status_id,
            location=equipment_data.location,
        )

        return EquipmentResponseSchema(
            id=equipment.id,
            name=equipment.name,
            current_status_id=equipment.current_status_id,
            location=equipment.location,
            last_heartbeat=equipment.last_heartbeat,
            created_at=equipment.created_at
        )
