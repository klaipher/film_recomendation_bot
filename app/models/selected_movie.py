from __future__ import annotations

from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin
from app.models.movie import Movie
from app.models.user import User


class SelectedMovie(TimestampedMixin, AbstractBaseModel):
    movie: fields.OneToOneRelation[Movie] = fields.OneToOneField(
        "models.Movie", to_field="id"
    )
    user: fields.OneToOneRelation[User] = fields.OneToOneField(
        "models.User", to_field="id"
    )

    class Meta:
        table = "selected_movies"
