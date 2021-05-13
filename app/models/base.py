from tortoise import Model, fields


class TimestampedMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class AbstractBaseModel(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True
