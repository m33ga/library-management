# Generated by Django 5.0.9 on 2025-01-08 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.PositiveIntegerField()),
                ('book_copy_id', models.PositiveIntegerField()),
                ('loan_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('returned_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loan')),
            ],
        ),
    ]
