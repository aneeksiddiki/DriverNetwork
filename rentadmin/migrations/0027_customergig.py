# Generated by Django 3.1.2 on 2020-12-30 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentadmin', '0026_auto_20201228_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customergig',
            fields=[
                ('gigid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('hours', models.IntegerField()),
                ('pickupdate', models.DateField()),
                ('pickuptime', models.TimeField()),
                ('vehicletype', models.CharField(max_length=200)),
                ('nagotiable', models.CharField(max_length=200)),
                ('stopable', models.CharField(max_length=200)),
                ('pickuploc', models.CharField(max_length=200)),
                ('droploc', models.CharField(max_length=200)),
                ('status', models.CharField(default='Active', max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('cid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rentadmin.customer')),
            ],
        ),
    ]
