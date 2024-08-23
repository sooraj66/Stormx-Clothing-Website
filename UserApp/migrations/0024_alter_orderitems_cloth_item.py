# Generated by Django 4.1.13 on 2024-08-18 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0008_alter_district_state'),
        ('UserApp', '0023_otp_mail_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='cloth_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='AdminApp.clothitems'),
        ),
    ]
