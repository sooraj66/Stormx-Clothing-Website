# Generated by Django 4.1.13 on 2024-08-14 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0008_alter_district_state'),
        ('UserApp', '0015_cart_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('order_items_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('cloth_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.clothitems')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.order')),
            ],
        ),
    ]
