# Generated by Django 3.1.2 on 2020-12-24 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0017_payments_pay_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='pay_plan',
            field=models.CharField(choices=[('5', '5 Miles - 5 USD'), ('10', '10 Miles - 10 USD'), ('15', '15 Miles - 15 USD'), ('20', '20 Miles - 20 USD')], max_length=200, null=True),
        ),
    ]