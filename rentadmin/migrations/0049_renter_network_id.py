# Generated by Django 3.1.2 on 2021-02-02 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0048_auto_20210203_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='network_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
