from django.contrib import admin
from .models import Customer
from .models import Loan


class CoustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'age' ,'monthly_salary', 'phone_number', 'approved_limit']
    search_fields = ['first_name', 'last_name', 'age' ,'monthly_salary', 'phone_number']

class LoanAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'loan_id', 'loan_amount' ,'interest_rate', 'monthly_installment', 'emis_paid_on_time']
    search_fields = ['first_name', 'last_name', 'age' ,'monthly_salary', 'phone_number']

admin.site.register(Customer, CoustomerAdmin)
admin.site.register(Loan, LoanAdmin)

