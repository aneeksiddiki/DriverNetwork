# Generated by Django 3.1.2 on 2021-01-18 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0043_car_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='gigride',
            name='counter_amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='gigride',
            name='counter_hours',
            field=models.IntegerField(null=True),
        ),
    ]
