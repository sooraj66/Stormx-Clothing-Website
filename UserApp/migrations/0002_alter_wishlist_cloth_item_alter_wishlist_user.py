# Generated by Django 4.1.13 on 2024-08-07 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0004_alter_clothspecification_cloth_item'),
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='cloth_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothitem', to='AdminApp.clothitems'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='UserApp.user'),
        ),
    ]
