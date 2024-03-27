from django.db import models

from base_model import BaseModel


class Loan(BaseModel):
    total_amount = models.FloatField()
    total_over_loan_term = models.FloatField()
    monthly_payment = models.FloatField()
    interest_rate = models.FloatField()
    mortgage_term = models.FloatField()  # Term in years
