# Generated by Django 4.1 on 2024-05-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0003_remove_offer_discountpercentage_offer_discount_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='minimum_purchase',
            field=models.IntegerField(default=0),
        ),
    ]
