# Generated by Django 3.1.2 on 2021-01-05 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0034_payments_pay_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='gigride',
            name='accept_date',
            field=models.DateField(null=True),
        ),
    ]
