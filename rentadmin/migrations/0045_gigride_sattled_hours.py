# Generated by Django 3.1.2 on 2021-01-19 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0044_auto_20210119_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='gigride',
            name='sattled_hours',
            field=models.IntegerField(null=True),
        ),
    ]