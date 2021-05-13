from __future__ import annotations

from enum import Enum

from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin


class Status(Enum):
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE"
    DEACTIVATED = "DEACTIVATED"


class User(TimestampedMixin, AbstractBaseModel):
    name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=40, null=True)
    status = fields.CharEnumField(Status, default=Status.ACTIVE, index=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.id}:{self.name}"
