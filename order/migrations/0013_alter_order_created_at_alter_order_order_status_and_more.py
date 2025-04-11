# Generated by Django 4.1 on 2024-09-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_order_status_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'Placed'), (1, 'Processing'), (2, 'Confirmed'), (3, 'Packing'), (4, 'Ready to Ship'), (5, 'Shipped'), (6, 'Cancelled'), (7, 'Pickup Requested'), (8, 'Assigned for Pickup'), (9, 'Picked'), (10, 'Pickup Failed'), (11, 'Pickup Cancelled'), (12, 'At the Sorting HUB'), (13, 'In Transit'), (14, 'Received at Last Mile HUB'), (15, 'Assigned for Delivery'), (16, 'Delivered'), (17, 'Partial Delivery'), (18, 'Return'), (19, 'Delivery Failed'), (20, 'On Hold'), (21, 'Payment Invoice'), (22, 'Paid Return'), (23, 'Exchange')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ordernote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
