# Generated by Django 3.1.2 on 2020-12-24 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0015_payments'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='txnid',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]
