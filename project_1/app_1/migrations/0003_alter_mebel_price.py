# Generated by Django 5.0.1 on 2024-01-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_mebel_delete_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mebel',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
