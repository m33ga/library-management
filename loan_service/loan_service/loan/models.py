from django.db import models
from datetime import timedelta

class Loan(models.Model):
    member_id = models.PositiveIntegerField(default=0)
    book_copy_id = models.PositiveIntegerField(default=0)
    loan_date = models.DateField(auto_now_add=True, blank=True, null=True)
    return_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"The book with the code {self.book_copy_id} was rented"

class Fine(models.Model):
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"The value of the fine is {self.amount}."