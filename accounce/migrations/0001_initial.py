# Generated by Django 4.1 on 2023-11-25 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('current_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('document_picture_url', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField()),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('invested_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('document_picture_url', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField()),
                ('investor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investments', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registered_investments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('withdraw_amount', models.PositiveIntegerField()),
                ('document_picture_url', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField()),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investment_withdraws', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registered_investment_withdraws', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfitShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=155)),
                ('description', models.TextField()),
                ('share_amount', models.PositiveIntegerField()),
                ('share_percentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_approved', models.BooleanField()),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=155)),
                ('description', models.TextField()),
                ('purchase_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_approved', models.BooleanField()),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('designation', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('work_day', models.PositiveIntegerField()),
                ('salary_amount', models.PositiveIntegerField()),
                ('is_approved', models.BooleanField()),
                ('is_paid', models.BooleanField()),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salaries', to=settings.AUTH_USER_MODEL)),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registered_salaries', to=settings.AUTH_USER_MODEL)),
                ('reporting_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('salary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.salary')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.CharField(max_length=255)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='ProfitShareRecived',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=155)),
                ('share_amount', models.PositiveIntegerField()),
                ('share_percentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField()),
                ('profit_share', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounce.profitshare')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfitShareApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('profit_share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.profitshare')),
            ],
        ),
        migrations.CreateModel(
            name='InvestorShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('share_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentWithdrawApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('investment_withdraw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.investmentwithdraw')),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.investment')),
            ],
        ),
        migrations.CreateModel(
            name='AccountBalanceApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField()),
                ('account_balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounce.accountbalance')),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
