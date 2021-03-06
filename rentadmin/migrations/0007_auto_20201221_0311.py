# Generated by Django 3.1.2 on 2020-12-20 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0006_auto_20201221_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberinfo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='primary_image',
            field=models.ImageField(default='none.jpg', upload_to='cars'),
        ),
    ]
