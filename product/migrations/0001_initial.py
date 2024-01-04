# Generated by Django 4.1 on 2023-12-26 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.PositiveBigIntegerField(default=product.models.Product.generate_unique_product_id, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sale_count', models.IntegerField(default=0)),
                ('visit_count', models.IntegerField(default=0)),
                ('wishlist_count', models.IntegerField(default=0)),
                ('quantity_in_stock', models.JSONField()),
                ('is_archived', models.BooleanField(default=False)),
                ('video_url', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('cover_picture', models.CharField(max_length=255)),
                ('profile_picture', models.CharField(max_length=255)),
                ('show_in_home_page', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('specification', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSizeChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('size_chart', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=30)),
                ('second_contact_number', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishListProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='product_tag_name_bf4b57_idx'),
        ),
        migrations.AddField(
            model_name='store',
            name='store_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='producttag',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='producttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.tag'),
        ),
        migrations.AddField(
            model_name='productsizechart',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='productphoto',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='productdescription',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcategory'),
        ),
        migrations.AddIndex(
            model_name='productcategory',
            index=models.Index(fields=['id'], name='product_pro_id_6b49fc_idx'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productdescription'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_size_chart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.productsizechart'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.store'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='wishlistproduct',
            index=models.Index(fields=['product'], name='product_wis_product_d8673d_idx'),
        ),
        migrations.AddIndex(
            model_name='wishlistproduct',
            index=models.Index(fields=['user'], name='product_wis_user_id_519b5b_idx'),
        ),
        migrations.AddConstraint(
            model_name='wishlistproduct',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique_wishlist'),
        ),
        migrations.AddIndex(
            model_name='store',
            index=models.Index(fields=['id'], name='product_sto_id_18adab_idx'),
        ),
        migrations.AddIndex(
            model_name='producttag',
            index=models.Index(fields=['product'], name='product_pro_product_8ea70a_idx'),
        ),
        migrations.AddIndex(
            model_name='producttag',
            index=models.Index(fields=['tag'], name='product_pro_tag_id_22f096_idx'),
        ),
        migrations.AddIndex(
            model_name='productsizechart',
            index=models.Index(fields=['product_category'], name='product_pro_product_db8d74_idx'),
        ),
        migrations.AddIndex(
            model_name='productsizechart',
            index=models.Index(fields=['id'], name='product_pro_id_4985f7_idx'),
        ),
        migrations.AddConstraint(
            model_name='productsizechart',
            constraint=models.UniqueConstraint(fields=('product_category', 'title'), name='unique_product_size_chart'),
        ),
        migrations.AddIndex(
            model_name='productphoto',
            index=models.Index(fields=['product'], name='product_pro_product_9799b2_idx'),
        ),
        migrations.AddIndex(
            model_name='productdescription',
            index=models.Index(fields=['product_category'], name='product_pro_product_22fe2c_idx'),
        ),
        migrations.AddIndex(
            model_name='productdescription',
            index=models.Index(fields=['id'], name='product_pro_id_b76f75_idx'),
        ),
        migrations.AddConstraint(
            model_name='productdescription',
            constraint=models.UniqueConstraint(fields=('product_category', 'title'), name='unique_product_description'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product_id'], name='product_pro_product_c0884e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product_category'], name='product_pro_product_ba1dca_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product_name'], name='product_pro_product_5af997_idx'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('product_id',), name='unique_product_id'),
        ),
        migrations.AddIndex(
            model_name='cartproduct',
            index=models.Index(fields=['product'], name='product_car_product_ee8178_idx'),
        ),
        migrations.AddIndex(
            model_name='cartproduct',
            index=models.Index(fields=['user'], name='product_car_user_id_11d69f_idx'),
        ),
        migrations.AddConstraint(
            model_name='cartproduct',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique_cart'),
        ),
    ]
