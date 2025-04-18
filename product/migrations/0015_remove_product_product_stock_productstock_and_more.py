# Generated by Django 4.1 on 2024-09-30 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_cartproduct_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_stock',
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='productstock',
            constraint=models.UniqueConstraint(fields=('product', 'size'), name='unique_product_stock'),
        ),
    ]
