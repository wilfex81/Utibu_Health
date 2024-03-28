# Generated by Django 5.0.3 on 2024-03-28 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_medication_name_alter_medication_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]