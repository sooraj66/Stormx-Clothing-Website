# Generated by Django 4.1.13 on 2024-08-14 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0008_alter_district_state'),
        ('UserApp', '0018_orderitems_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cloth_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothitemcart', to='AdminApp.clothitems'),
        ),
    ]
