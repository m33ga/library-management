# Generated by Django 5.0.9 on 2025-01-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_remove_loan_book_copy_id_remove_loan_member_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='book_copy_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='loan',
            name='member_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='loan',
            name='returned_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
