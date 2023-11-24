from django.db import models

from authentication.models import User


class Purchase(models.Model):
    created_at = models.DateField(auto_now_add=True, editable=False)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    title = models.CharField(max_length=155)
    description = models.TextField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField()


class PurchaseApproval(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField()


class PurchasePhoto(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=255)


class AccountBalance(models.Model):
    created_at = models.DateField(auto_now_add=True, editable=False)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    document_picture_url = models.CharField(max_length=255)
    is_approved = models.BooleanField()


class AccountBalanceApproval(models.Model):
    account_balance = models.ForeignKey(
        AccountBalance, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField()


class Investment(models.Model):
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True, editable=False)

    investor = models.ForeignKey(User, on_delete=models.SET_NULL)
    invested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    document_picture_url = models.CharField(max_length=255)
    is_approved = models.BooleanField()


class InvestmentApproval(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField()


class InvestorShare(models.Model):
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    share_value = models.DecimalField(max_digits=10, decimal_places=2)


class Salary(models.Model):
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True, editable=False)

    employee = models.ForeignKey(User, on_delete=models.SET_NULL)
    reporting_manager = models.ForeignKey(User, on_delete=models.SET_NULL)

    designation = models.CharField(max_length=50)
    comment = models.TextField()
    work_day = models.PositiveIntegerField()
    salary_amount = models.PositiveIntegerField()

    is_approved = models.BooleanField()
    is_paid = models.BooleanField()


class SalaryApproval(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL)
    is_approved = models.BooleanField()


class InvestmentWithdraw(models.Model):
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True, editable=False)

    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    withdraw_amount = models.PositiveIntegerField()
    document_picture_url = models.CharField(max_length=255)
    is_approved = models.BooleanField()


class InvestmentWithdrawApproval(models.Model):
    investment_withdraw = models.ForeignKey(
        InvestmentWithdraw, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL)
    is_approved = models.BooleanField()


class ProfitShare(models.Model):
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True, editable=False)

    title = models.CharField(max_length=155)
    description = models.TextField()

    share_amount = models.PositiveIntegerField()
    share_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField()


class ProfitShareApproval(models.Model):
    profit_share = models.ForeignKey(ProfitShare, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL)
    is_approved = models.BooleanField()


class ProfitShareRecived(models.Model):
    profit_share = models.ForeignKey(ProfitShare, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True, editable=False)

    title = models.CharField(max_length=155)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    share_amount = models.PositiveIntegerField()
    share_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField()
