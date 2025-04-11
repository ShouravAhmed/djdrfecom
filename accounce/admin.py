from django.contrib import admin

from .models import *

admin.site.register(Purchase)
admin.site.register(PurchaseApproval)
admin.site.register(PurchaseImage)
admin.site.register(AccountBalance)
admin.site.register(AccountBalanceApproval)
admin.site.register(Investment)
admin.site.register(InvestorShare)
admin.site.register(Salary)
admin.site.register(SalaryApproval)
admin.site.register(InvestmentWithdraw)
admin.site.register(InvestmentWithdrawApproval)
admin.site.register(ProfitShare)
admin.site.register(ProfitShareApproval)
admin.site.register(ProfitShareRecived)
