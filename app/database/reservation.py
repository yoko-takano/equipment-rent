from tortoise import fields, models
import uuid


class Reservation(models.Model):
    """
    Stores information about reservations made by users.

    Attributes:
        id (UUID): Unique identifier of the reservation.
        user_id (User): User who made the reservation.
        equipment_id (Equipment): Reserved equipment.
        start_time (datetime): Reservation start time.
        end_time (datetime): Reservation end time.
        status_id (ReservationStatus): Reservation status.
        created_at (datetime): Reserved equipment.
    """
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user_id = fields.ForeignKeyField(
        "database.User",
        related_name="reservations",
        null=False
    )
    equipment_id = fields.ForeignKeyField(
        "database.Equipment",
        related_name="reservations",
        null=False
    )
    start_time = fields.DatetimeField(null=False)
    end_time = fields.DatetimeField(null=False)
    status_id = fields.ForeignKeyField(
        "database.ReservationStatus",
        related_name="reservations",
        null=False
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "reservations"
        ordering = ["-created_at"]
