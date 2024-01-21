"""Movies configuration for admin panel."""
from django.contrib import admin

import movies.models as mdl


# Inlines

class PersonFilmInline(admin.TabularInline):
    """Inline table PersonFilmwork for FilmworkAdmin."""

    model = mdl.PersonFilm


class GenreFilmInline(admin.TabularInline):
    """Inline table GenreFilm for FilmAdmin."""

    model = mdl.GenreFilm


# Registrations

@admin.register(mdl.Person)
class PersonAdmin(admin.ModelAdmin):
    """Adding the Person table to the admin panel."""

    list_display = ('fullname',)
    search_fields = ('id', 'fullname',)


@admin.register(mdl.Genre)
class GenreAdmin(admin.ModelAdmin):
    """Adding the Genre table to the admin panel."""

    list_display = ('name', 'description',)
    search_fields = ('id', 'name', 'description',)


@admin.register(mdl.Film)
class FilmworkAdmin(admin.ModelAdmin):
    """Adding the Film table to the admin panel."""

    # Использование вложенных форм
    inlines = (PersonFilmInline, GenreFilmInline,)

    # Отображение полей в списке
    list_display = ('title', 'creation_date', 'rating', 'film_type', 'created', 'modified',)

    # Фильтрация в списке
    list_filter = ('film_type',)

    # Поиск по полям
    search_fields = ('id', 'title', 'description',)
