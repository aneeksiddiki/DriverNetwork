# Generated by Django 3.1.2 on 2021-02-05 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0061_auto_20210206_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riderequest',
            old_name='customer_network_id',
            new_name='customer_network_code',
        ),
    ]
