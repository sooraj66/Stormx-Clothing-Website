# Generated by Django 4.1.13 on 2024-08-15 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0020_user_otp_user_otp_expiration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
