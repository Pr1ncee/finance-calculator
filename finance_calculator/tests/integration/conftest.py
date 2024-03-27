import pytest

from loan_calculator.models import Loan


@pytest.fixture
def test_loan_data():
    return {
        "total_amount": 100000,
        "total_over_loan_term": 20000,
        "mortgage_term": 5,
        "interest_rate": 4.5,
        "monthly_payment": 2000,
    }


@pytest.fixture
def test_loan_obj(test_loan_data):
    loan = Loan.objects.create(**test_loan_data)
    yield loan
    loan.delete()
