# Generated by Django 3.1.2 on 2020-12-20 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0004_auto_20201221_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='chauffeur',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=200),
        ),
    ]
