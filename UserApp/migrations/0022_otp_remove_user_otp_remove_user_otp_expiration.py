# Generated by Django 4.1.13 on 2024-08-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0021_alter_order_shipping_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_expiration', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_expiration',
        ),
    ]
