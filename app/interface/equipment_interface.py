from abc import ABC, abstractmethod


class IEquipmentService(ABC):
    """
    Interface class responsible for equipment-related operations.
    """
    @classmethod
    @abstractmethod
    async def get_equipment_statuses(cls):
        """
        Retrieves all possible equipment statuses.
        """
        raise NotImplementedError()
