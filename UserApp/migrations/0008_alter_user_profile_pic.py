# Generated by Django 4.1.13 on 2024-08-10 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
