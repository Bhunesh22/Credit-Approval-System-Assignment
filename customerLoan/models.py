from django.db import models
from datetime import date


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.BigIntegerField()
    monthly_salary = models.BigIntegerField()
    approved_limit = models.BigIntegerField(blank=True)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return str(self.first_name)

class Loan(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.IntegerField()
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()

    class Meta:
        db_table = 'loan'

    def __str__(self):
        return str(self.loan_id)
