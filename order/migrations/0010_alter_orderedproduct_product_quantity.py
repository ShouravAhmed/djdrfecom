# Generated by Django 4.1 on 2024-08-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_remove_orderedproduct_unique_ordered_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='product_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
