# Generated by Django 5.0.3 on 2024-03-28 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='medications',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.medication'),
        ),
    ]
