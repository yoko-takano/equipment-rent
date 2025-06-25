from datetime import datetime

from tortoise import fields
from tortoise.models import Model
import uuid

from tools.application import naive_utcnow


class Equipment(Model):
    """
    Stores the equipment available in the system.

    Attributes:
        id (UUID): Unique identifier of the equipment.
        name (str): Name of the equipment.
        current_status_id (EquipmentStatus): Current status of the equipment.
        location (UUID): Location of the equipment.
        last_heartbeat (datetime): Last communication timestamp from the equipment.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=60, unique=True, null=False)
    current_status_id = fields.ForeignKeyField(
        "models.EquipmentStatus",
        related_name="equipments",
        null=True
    )
    location = fields.UUIDField(null=True)
    last_heartbeat = fields.DatetimeField(null=False, default=naive_utcnow)
    created_at = fields.DatetimeField(null=False, default=naive_utcnow)

    class Meta:
        table = "Equipments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.current_status_id}>"
