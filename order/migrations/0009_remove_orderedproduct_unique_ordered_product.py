# Generated by Django 4.1 on 2024-08-25 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_orderedproduct_unique_ordered_product'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='orderedproduct',
            name='unique_ordered_product',
        ),
    ]
