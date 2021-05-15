from __future__ import annotations

from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin
from app.models.movie import Movie
from app.models.user import User


class MovieRating(TimestampedMixin, AbstractBaseModel):
    movie: fields.ForeignKeyRelation[Movie] = fields.ForeignKeyField(
        "models.Movie", to_field="id"
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", to_field="id"
    )
    rating = fields.SmallIntField(null=True)
    didnt_see = fields.BooleanField(default=False)

    class Meta:
        table = "movie_ratings"
