# Generated by Django 5.0.1 on 2024-01-21 22:39

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_create_content_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('film_type', models.TextField(choices=[('movie', 'movie'), ('tv_show', 'tv_show')], default='movie', verbose_name='film_type')),
            ],
            options={
                'verbose_name': 'film',
                'verbose_name_plural': 'films',
                'db_table': 'content"."film',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.TextField(verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('fullname', models.TextField(verbose_name='fullname')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='GenreFilm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.film', verbose_name='film')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='genre')),
            ],
            options={
                'verbose_name': 'genre_film',
                'verbose_name_plural': 'genre_films',
                'db_table': 'content"."genre_film',
                'unique_together': {('genre', 'film')},
            },
        ),
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilm', to='movies.genre'),
        ),
        migrations.CreateModel(
            name='PersonFilm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('person_role', models.TextField(choices=[('actor', 'actor'), ('writer', 'writer'), ('director', 'director')], default='actor', verbose_name='person_role')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.film', verbose_name='film')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='person')),
            ],
            options={
                'verbose_name': 'person_film',
                'verbose_name_plural': 'person_films',
                'db_table': 'content"."person_film',
                'unique_together': {('person', 'film', 'person_role')},
            },
        ),
        migrations.AddField(
            model_name='film',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilm', to='movies.person'),
        ),
    ]
