# Generated by Django 4.1.13 on 2024-08-02 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothitems',
            name='stock',
            field=models.CharField(max_length=100),
        ),
    ]
