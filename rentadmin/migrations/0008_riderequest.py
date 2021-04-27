# Generated by Django 3.1.2 on 2020-12-21 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0007_auto_20201221_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('requestid', models.AutoField(primary_key=True, serialize=False)),
                ('request_type', models.CharField(default='General', max_length=200)),
                ('lat', models.CharField(max_length=200, null=True)),
                ('long', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('cid', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rentadmin.customer')),
            ],
        ),
    ]