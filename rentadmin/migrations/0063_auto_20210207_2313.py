# Generated by Django 3.1.2 on 2021-02-07 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0062_auto_20210206_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='network_root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='network_root', to='rentadmin.renter'),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride_driver', to='rentadmin.renter'),
        ),
    ]
