"""Movies models."""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


# Mixins

class UUIDMixin(models.Model):
    """Mixin for adding uuid."""

    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы.
        abstract = True


class TimeStampedMixin(models.Model):
    """Mixin for adding created and modified timestamp."""

    created = models.DateTimeField(
        _('created'),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        _('modified'),
        auto_now=True,
    )

    class Meta:
        abstract = True


# Enums

class FilmTypeEnum(models.TextChoices):
    """Enum for film types."""

    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('tv_show')


class FilmRoleEnum(models.TextChoices):
    """Enum for roles types."""

    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


# Validators

rating_validator = [
    MinValueValidator(0),
    MaxValueValidator(100),
]


# Tables

class Person(UUIDMixin, TimeStampedMixin):
    """Description for the Person table."""

    fullname = models.TextField(
        _('fullname'),
        blank=False,
        null=False,
    )

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.fullname


class Genre(UUIDMixin, TimeStampedMixin):
    """Description for the Genre table."""

    name = models.TextField(
        _('name'),
        blank=False,
        null=False,
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Film(UUIDMixin, TimeStampedMixin):
    """Description for the Film table."""

    title = models.TextField(
        _('title'),
        # blank=False делает поле обязательным для заполнения на уровне Django.
        blank=False,
        null=False,
    )
    description = models.TextField(
        _('description'),
        # blank=True делает поле необязательным для заполнения на уровне Django.
        blank=True,
        null=True,
    )
    creation_date = models.DateField(
        _('creation_date'),
        # blank=True делает поле необязательным для заполнения на уровне Django.
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=rating_validator,
    )
    film_type = models.TextField(
        _('film_type'),
        choices=FilmTypeEnum,
        default=FilmTypeEnum.MOVIE,
    )
    persons = models.ManyToManyField(
        Person,
        through='PersonFilm',
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilm',
    )

    class Meta:
        # Tаблица film находятся в нестандартной схеме content.
        db_table = 'content"."film'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title


class PersonFilm(UUIDMixin):
    """
    Description for the PersonFilm table.

    This table is for the many-to-many relationship.
    Between Persons and Films.
    """

    person = models.ForeignKey(
        'Person',
        verbose_name=_('person'),
        on_delete=models.CASCADE,
    )
    film = models.ForeignKey(
        'Film',
        verbose_name=_('film'),
        on_delete=models.CASCADE,
    )
    person_role = models.TextField(
        _('person_role'),
        choices=FilmRoleEnum.choices,
        default=FilmRoleEnum.ACTOR,
    )
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content"."person_film'
        verbose_name = _('person_film')
        verbose_name_plural = _('person_films')
        unique_together = ('person', 'film', 'person_role')

    def __str__(self):
        return f'Person: {self.person}, Film: {self.film}, Role: {self.person_role}'


class GenreFilm(UUIDMixin):
    """
    Description for the GenreFilm table.

    This table is for the many-to-many relationship.
    Between Genres and Films.
    """

    genre = models.ForeignKey(
        'Genre',
        verbose_name=_('genre'),
        on_delete=models.CASCADE,
    )
    film = models.ForeignKey(
        'Film',
        verbose_name=_('film'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True,
    )

    class Meta:
        db_table = 'content"."genre_film'
        verbose_name = _('genre_film')
        verbose_name_plural = _('genre_films')
        unique_together = ('genre', 'film')

    def __str__(self):
        return f'Genre: {self.genre}, Film: {self.film}'
