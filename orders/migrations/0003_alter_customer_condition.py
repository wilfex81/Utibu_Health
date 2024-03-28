# Generated by Django 5.0.3 on 2024-03-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_medication_price_alter_order_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='condition',
            field=models.CharField(choices=[('HIV', 'HIV'), ('HYPERTENSION', 'hypertension'), ('DIABETES', 'diabetes')], default='', max_length=255),
        ),
    ]