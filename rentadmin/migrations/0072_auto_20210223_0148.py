# Generated by Django 3.1.6 on 2021-02-22 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0071_auto_20210210_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riderequest',
            old_name='lat',
            new_name='dstlat',
        ),
        migrations.RemoveField(
            model_name='riderequest',
            name='lon',
        ),
        migrations.AddField(
            model_name='riderequest',
            name='dstlon',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='picklat',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='picklon',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
