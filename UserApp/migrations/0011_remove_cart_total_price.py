# Generated by Django 4.1.13 on 2024-08-11 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0010_alter_cart_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
    ]
