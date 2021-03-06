# Generated by Django 3.1.2 on 2021-02-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0069_auto_20210210_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='renter',
            name='points',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
