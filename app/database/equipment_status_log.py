from tortoise import fields, models
import uuid


class EquipmentStatusLog(models.Model):
    """
    Stores the status change logs of the equipment.

    Attributes:
        id (UUID): Unique identifier of the equipment status log.
        status_id (EquipmentStatus): Registered equipment status.
        equipment_id (Equipment): Corresponding equipment.
        details (str): Additional information about the status change.
        reported_at (datetime): Date and time of the event.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    status_id = fields.ForeignKeyField(
        "database.EquipmentStatus",
        related_name="status_logs",
        null=False
    )
    equipment_id = fields.ForeignKeyField(
        "database.Equipment",
        related_name="status_logs",
        null=False
    )
    details = fields.CharField(max_length=300, null=True)
    reported_at = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "equipment_status_logs"
        ordering = ["-created_at"]
