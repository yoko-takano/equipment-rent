from tortoise import fields, models
import uuid


class CommandType(models.Model):
    """
    Defines the different types of commands that can be sent to equipment.

    Attributes:
        id (UUID): Unique identifier of the command type.
        name (str): Name of the command type.
        created_at (datetime): Record creation timestamp.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=60, unique=True, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "command_types"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
