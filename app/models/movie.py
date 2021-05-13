from __future__ import annotations

from tortoise import fields

from app.models.base import AbstractBaseModel, TimestampedMixin


class Movie(TimestampedMixin, AbstractBaseModel):
    name = fields.CharField(max_length=255)
    genres: fields.ManyToManyRelation[Genre] = fields.ManyToManyField(
        "models.Genre", through="movie_genre", to_field="id"
    )
    year = fields.IntField()
    description = fields.TextField()
    directors: fields.ManyToManyRelation[Director] = fields.ManyToManyField(
        "models.Director", through="movie_director", to_field="id"
    )
    actors: fields.ManyToManyRelation[Actor] = fields.ManyToManyField(
        "models.Actor", through="movie_actor", to_field="id"
    )

    class Meta:
        table = "movies"

    def __repr__(self):
        return f"<Movie: {self.name}"


class Genre(AbstractBaseModel):
    name = fields.CharField(max_length=255)

    class Meta:
        table = "genres"

    def __repr__(self):
        return f"<Genre: {self.name}"


class Director(AbstractBaseModel):
    name = fields.CharField(max_length=255)

    class Meta:
        table = "directors"

    def __repr__(self):
        return f"<Director: {self.name}"


class Actor(AbstractBaseModel):
    name = fields.CharField(max_length=255)

    class Meta:
        table = "actors"

    def __repr__(self):
        return f"<Actor: {self.name}"
