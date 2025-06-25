from app.interface.equipment_interface import IEquipmentService


class EquipmentPersistence(IEquipmentService):
    """
    Persistence class responsible for equipment-related operations.
    """
    @classmethod
    async def get_equipment_statuses(cls):
        """
        Retrieves all possible equipment statuses.
        """
        pass

