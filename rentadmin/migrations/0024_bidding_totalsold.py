# Generated by Django 3.1.2 on 2020-12-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0023_bidding'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding',
            name='totalsold',
            field=models.IntegerField(default=0),
        ),
    ]
