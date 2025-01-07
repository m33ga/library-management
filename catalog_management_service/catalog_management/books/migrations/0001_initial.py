# Generated by Django 5.0.9 on 2025-01-05 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_year', models.PositiveIntegerField()),
                ('total_books', models.PositiveIntegerField(default=1)),
                ('available_books', models.PositiveIntegerField(default=1)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='books.author')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='books.genre')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.institution')),
            ],
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved')], default='available', max_length=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='books.book')),
            ],
        ),
    ]
