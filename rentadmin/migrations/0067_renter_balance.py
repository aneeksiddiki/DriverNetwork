# Generated by Django 3.1.2 on 2021-02-09 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0066_auto_20210208_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]