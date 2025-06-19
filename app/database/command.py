from tortoise import fields, models
import uuid


class Command(models.Model):
    """
    Records commands sent to equipment.

    Attributes:
        id (UUID): Unique identifier of the command.
        command_type (CommandType): Name of the command type.
        equipment_id (Equipment): Equipment that will receive the command.
        payload (str): Command data.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    command_type = fields.ForeignKeyField(
        "database.CommandType",
        related_name="commands",
        null=False
    )
    equipment_id = fields.ForeignKeyField(
        "database.Equipment",
        related_name="commands",
        null=False
    )
    payload = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "commands"
        ordering = ["-created_at"]
