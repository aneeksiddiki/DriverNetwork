# Generated by Django 3.1.2 on 2021-02-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0070_auto_20210210_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='points',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
