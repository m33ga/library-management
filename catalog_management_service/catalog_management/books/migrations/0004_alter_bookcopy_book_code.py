# Generated by Django 5.0.9 on 2025-01-05 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_bookcopy_book_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcopy',
            name='book_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
