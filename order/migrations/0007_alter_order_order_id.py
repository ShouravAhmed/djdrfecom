# Generated by Django 4.1 on 2024-08-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
