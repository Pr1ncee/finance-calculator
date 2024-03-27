import pytest
from rest_framework import status

from loan_calculator.models import Loan
from loan_calculator.services.loan import LoanCalculator


class TestLoanCalculator:
    @pytest.mark.parametrize(
        "mortgage_term_in_months, expected_years",
        [
            (90, 7.5),
            (48, 4),
            (30, 2.5),
        ],
    )
    def test_calculate_mortgage_term_in_years(
        self, mortgage_term_in_months, expected_years
    ):
        result = LoanCalculator.calculate_mortgage_term_in_years(
            mortgage_term_in_months
        )
        assert result == expected_years

    @pytest.mark.parametrize(
        "total_amount, loan_amount, expected_total_interest",
        [
            (100000, 80000, 20000),
            (150000, 120000, 30000),
        ],
    )
    def test_calculate_total_interest_over_loan_term(
        self, total_amount, loan_amount, expected_total_interest
    ):
        result = LoanCalculator.calculate_total_interest_over_loan_term(
            total_amount, loan_amount
        )
        assert result == expected_total_interest

    @pytest.mark.parametrize(
        "monthly_payment, mortgage_term_in_months, expected_total_over_loan_term",
        [
            (1000, 12, 12000),
            (1500, 24, 36000),
        ],
    )
    def test_calculate_total_over_loan_term(
        self, monthly_payment, mortgage_term_in_months, expected_total_over_loan_term
    ):
        result = LoanCalculator.calculate_total_over_loan_term(
            monthly_payment, mortgage_term_in_months
        )
        assert result == expected_total_over_loan_term

    @pytest.mark.parametrize(
        "loan_amount, interest_rate, mortgage_term_in_months, expected_monthly_payment",
        [
            (100000, 0.05, 12, 8335.59),
            (150000, 0.06, 24, 6253.91),
        ],
    )
    def test_calculate_monthly_payment(
        self,
        loan_amount,
        interest_rate,
        mortgage_term_in_months,
        expected_monthly_payment,
    ):
        result = LoanCalculator.calculate_monthly_payment(
            loan_amount, interest_rate, mortgage_term_in_months
        )
        assert result == expected_monthly_payment

    @pytest.mark.parametrize(
        "purchase_price, down_payment, expected_loan_amount",
        [
            (100000, 20000, 80000),
            (150000, 30000, 120000),
        ],
    )
    def test_calculate_total_loan_amount(
        self, purchase_price, down_payment, expected_loan_amount
    ):
        result = LoanCalculator.calculate_total_loan_amount(
            purchase_price, down_payment
        )
        assert result == expected_loan_amount

    @pytest.mark.parametrize(
        "purchase_price, dollar_down_payment, percentage_down_payment, expected_down_payment",
        [
            (100000, 20000, None, 20000),
            (100000, None, 0.2, 20000),
        ],
    )
    def test_get_down_payment(
        self,
        purchase_price,
        dollar_down_payment,
        percentage_down_payment,
        expected_down_payment,
    ):
        result = LoanCalculator.get_down_payment(
            purchase_price, dollar_down_payment, percentage_down_payment
        )
        assert result == expected_down_payment

    def test_get_down_payment_error(self):
        result = LoanCalculator.get_down_payment(100000, None, None)
        assert result is None

    def test_calculate_loan(self):
        result = LoanCalculator.calculate_loan(
            purchase_price=100000.15,
            interest_rate=20.1,
            dollar_down_payment=10000,
            percentage_down_payment=None,
            mortgage_term=48,
        )
        expected_results = (90000.15, 2743.53, 131689.44, 0.0)
        for e, v in zip(result, expected_results):
            assert e == v

    @pytest.mark.django_db
    def test_save_loan(self):
        mortgage_term_in_years = 5
        monthly_payment = 9999.9
        interest_rate = 25
        total_amount = 1500000
        total_over_loan_term = 25000.15

        result = LoanCalculator.save_loan(
            mortgage_term_in_years=mortgage_term_in_years,
            monthly_payment=monthly_payment,
            interest_rate=interest_rate,
            total_amount=total_amount,
            total_over_loan_term=total_over_loan_term,
        )
        assert result["error"] is False
        assert result["msg"] == "Success!"
        assert result["status"] == status.HTTP_201_CREATED

        all_loans = Loan.objects.all()
        assert all_loans.count() == 1
        assert all_loans[0].mortgage_term == mortgage_term_in_years
        assert all_loans[0].monthly_payment == monthly_payment
        assert all_loans[0].interest_rate == interest_rate
        assert all_loans[0].total_amount == total_amount
        assert all_loans[0].total_over_loan_term == total_over_loan_term

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "mortgage_term_in_years, monthly_payment, interest_rate, total_amount, total_over_loan_term",
        [
            (5, 9999.9, 25, None, 25000.15),
            (5, 9999.9, 25, "invalid number", 25000.15),
            (5, None, 25, 20000, 25000.15),
            (5, 9999.9, None, "invalid number", 25000.15),
            (None, 9999.9, 25, 20000, 25000.15),
        ],
    )
    def test_save_loan_fail(
        self,
        mortgage_term_in_years,
        monthly_payment,
        interest_rate,
        total_amount,
        total_over_loan_term,
    ):
        result = LoanCalculator.save_loan(
            mortgage_term_in_years=mortgage_term_in_years,
            monthly_payment=monthly_payment,
            interest_rate=interest_rate,
            total_amount=total_amount,
            total_over_loan_term=total_over_loan_term,
        )
        assert result["error"] is True
        assert result["msg"] == "Error! Invalid input arguments!"
        assert result["status"] == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_calculate_and_save_loan(self):
        result = LoanCalculator.calculate_and_save_loan(
            purchase_price=100000,
            interest_rate=20,
            dollar_down_payment=10000,
            percentage_down_payment=None,
            mortgage_term=90,
        )
        assert result["status"] == status.HTTP_201_CREATED
        assert result["data"]["total_amount"] == 90000
        assert result["data"]["monthly_payment"] == 1937.75
        assert result["data"]["total_over_loan_term"] == 174397.5
        assert result["data"]["total_interest_paid_over_loan_term"] == 0.0
        assert result["data"]["mortgage_term_in_years"] == 7.5

    @pytest.mark.django_db
    def test_calculate_and_save_loan_fail(self):
        with pytest.raises(TypeError):
            LoanCalculator.calculate_and_save_loan(
                purchase_price=100000,
                interest_rate=20,
                dollar_down_payment=None,
                percentage_down_payment=None,
                mortgage_term=90,
            )
