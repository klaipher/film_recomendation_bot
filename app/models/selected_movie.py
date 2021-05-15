from __future__ import annotations

from typing import List

from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin
from app.models.movie import Movie
from app.models.user import User


class SelectedMovie(TimestampedMixin, AbstractBaseModel):
    movie: fields.ForeignKeyRelation[Movie] = fields.ForeignKeyField(
        "models.Movie", to_field="id"
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", to_field="id"
    )

    class Meta:
        table = "selected_movies"

    @classmethod
    async def paginate(cls: SelectedMovie, page: int, filters: dict = None, paginate_by=1) -> List[SelectedMovie]:
        if filters is None:
            filters = {}

        if page > 0:
            page -= 1
        _limit = paginate_by
        _offset = page * paginate_by

        results = await cls.filter(**filters).limit(_limit).offset(_offset)
        return results

    @classmethod
    async def count(cls: SelectedMovie, filters: dict = None):
        if filters is None:
            filters = {}
        return await cls.filter(**filters).all().count()
