# Generated by Django 3.1.2 on 2021-02-07 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0065_auto_20210208_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderequest',
            name='status',
            field=models.CharField(default='Pending', max_length=200),
        ),
    ]