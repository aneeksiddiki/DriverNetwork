# Generated by Django 3.1.2 on 2020-12-20 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberinfo',
            name='cid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rentadmin.customer'),
        ),
    ]
