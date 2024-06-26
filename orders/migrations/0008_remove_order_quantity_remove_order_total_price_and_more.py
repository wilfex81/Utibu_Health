# Generated by Django 5.0.3 on 2024-03-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_medication_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='medications',
        ),
        migrations.AddField(
            model_name='order',
            name='medications',
            field=models.ManyToManyField(to='orders.medication'),
        ),
    ]
