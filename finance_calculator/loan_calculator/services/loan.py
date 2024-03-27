from typing import Any

from django.db import IntegrityError
from rest_framework import status

from loan_calculator.models import Loan


class LoanCalculator:
    """
    A class to calculate and save loan details.

    Attributes:
        None

    Methods:
        calculate_and_save_loan: Calculate loan details and save them to the database.
        calculate_loan: Calculate various loan details based on given parameters.
        save_loan: Save loan details to the database.
        get_down_payment: Calculate the down payment amount.
        calculate_total_loan_amount: Calculate the total loan amount.
        calculate_monthly_payment: Calculate the monthly payment amount.
        calculate_total_over_loan_term: Calculate the total payment over the loan term.
        calculate_total_interest_over_loan_term: Calculate the total interest paid over the loan term.
        calculate_mortgage_term_in_years: Convert mortgage term from months to years.
    """

    @classmethod
    def calculate_and_save_loan(
        cls,
        purchase_price: float,
        interest_rate: float,
        dollar_down_payment: float | None,
        percentage_down_payment: float | None,
        mortgage_term: int,
    ) -> dict[str, dict[str, status] | str]:
        """
        Calculate loan details and save them to the database.

        Args:
            purchase_price (float): The purchase price of the loan.
            interest_rate (float): The interest rate of the loan.
            dollar_down_payment (float | None): The down payment in dollars.
            percentage_down_payment (float | None): The down payment as a percentage of the purchase price.
            mortgage_term (int): The mortgage term in months.

        Returns:
            dict[str, dict[str, status] | str]: A dictionary containing either calculated loan details or error message.
        """

        (
            total_amount,
            monthly_payment,
            total_over_loan_term,
            total_interest_paid_over_loan_term,
        ) = cls.calculate_loan(
            purchase_price=purchase_price,
            interest_rate=interest_rate,
            dollar_down_payment=dollar_down_payment,
            percentage_down_payment=percentage_down_payment,
            mortgage_term=mortgage_term,
        )

        mortgage_term_in_years = cls.calculate_mortgage_term_in_years(
            mortgage_term=mortgage_term
        )
        response = cls.save_loan(
            mortgage_term_in_years=mortgage_term_in_years,
            total_amount=total_amount,
            monthly_payment=monthly_payment,
            total_over_loan_term=total_over_loan_term,
            interest_rate=total_interest_paid_over_loan_term,
        )
        loan_details = {
            "total_amount": total_amount,
            "monthly_payment": monthly_payment,
            "total_over_loan_term": total_over_loan_term,
            "total_interest_paid_over_loan_term": total_interest_paid_over_loan_term,
            "mortgage_term_in_years": mortgage_term_in_years,
        }
        return {
            "data": response["msg"] if response["error"] else loan_details,
            "status": response["status"],
        }

    @classmethod
    def calculate_loan(
        cls,
        purchase_price: float,
        interest_rate: float,
        dollar_down_payment: float | None,
        percentage_down_payment: float | None,
        mortgage_term: int,
    ) -> tuple[float, float, float, float]:
        """
        Calculate various loan details based on given parameters.

        Args:
            purchase_price (float): The purchase price of the loan.
            interest_rate (float): The interest rate of the loan.
            dollar_down_payment (float | None): The down payment in dollars.
            percentage_down_payment (float | None): The down payment as a percentage of the purchase price.
            mortgage_term (int): The mortgage term in months.

        Returns:
            tuple[float, float, float, float]: A tuple containing calculated loan details.
        """

        down_payment = cls.get_down_payment(
            purchase_price=purchase_price,
            dollar_down_payment=dollar_down_payment,
            percentage_down_payment=percentage_down_payment,
        )
        total_amount = cls.calculate_total_loan_amount(
            purchase_price=purchase_price, down_payment=down_payment
        )
        monthly_payment = cls.calculate_monthly_payment(
            loan_amount=total_amount,
            mortgage_term_in_months=mortgage_term,
            interest_rate=interest_rate,
        )
        total_over_loan_term = cls.calculate_total_over_loan_term(
            monthly_payment=monthly_payment, mortgage_term_in_months=mortgage_term
        )
        total_interest_paid_over_loan_term = (
            cls.calculate_total_interest_over_loan_term(
                total_over_loan_term=total_over_loan_term,
                loan_amount=total_over_loan_term,
            )
        )
        return (
            total_amount,
            monthly_payment,
            total_over_loan_term,
            total_interest_paid_over_loan_term,
        )

    @classmethod
    def save_loan(
        cls,
        mortgage_term_in_years: float,
        monthly_payment: float,
        interest_rate: float,
        total_amount: float,
        total_over_loan_term: float,
    ) -> dict[str, str | bool | Any]:
        """
        Save loan details to the database.

        Args:
            mortgage_term_in_years (float): The mortgage term in years.
            monthly_payment (float): The monthly payment amount.
            interest_rate (float): The interest rate of the loan.
            total_amount (float): The total loan amount.
            total_over_loan_term (float): The total payment over the loan term.

        Returns:
            dict[str, int]: Either success response status or dict consists of error message and HTTP status code.
        """
        try:
            Loan.objects.create(
                total_amount=total_amount,
                total_over_loan_term=total_over_loan_term,
                mortgage_term=mortgage_term_in_years,
                interest_rate=interest_rate,
                monthly_payment=monthly_payment,
            )
        except (ValueError, TypeError, IntegrityError):
            return {
                "msg": "Error! Invalid input arguments!",
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
            }
        else:
            return {
                "msg": "Success!",
                "status": status.HTTP_201_CREATED,
                "error": False,
            }

    @staticmethod
    def get_down_payment(
        purchase_price: float,
        dollar_down_payment: float | None,
        percentage_down_payment: float | None,
    ) -> float:
        """
        Calculate the down payment amount.

        Args:
            purchase_price (float): The purchase price of the loan.
            dollar_down_payment (float | None): The down payment in dollars.
            percentage_down_payment (float | None): The down payment as a percentage of the purchase price.

        Returns:
            float: The calculated down payment amount.
        """
        down_payment = (
            purchase_price * percentage_down_payment
            if percentage_down_payment
            else dollar_down_payment
        )
        return round(down_payment, 2) if down_payment else None

    @staticmethod
    def calculate_total_loan_amount(
        purchase_price: float, down_payment: float
    ) -> float:
        """
        Calculate the total loan amount.

        Args:
            purchase_price (float): The purchase price of the loan.
            down_payment (float): The down payment amount.

        Returns:
            float: The total loan amount.
        """

        return round(purchase_price - down_payment, 2)

    @staticmethod
    def calculate_monthly_payment(
        loan_amount: float, interest_rate: float, mortgage_term_in_months: int
    ) -> float:
        """
        Calculate the monthly payment amount.

        Args:
            loan_amount (float): The total loan amount.
            interest_rate (float): The interest rate of the loan.
            mortgage_term_in_months (int): The mortgage term in months.

        Returns:
            float: The monthly payment amount.
        """

        monthly_interest_rate = interest_rate / (12 * 100)
        return round(
            (
                loan_amount
                * (
                    monthly_interest_rate
                    * (1 + monthly_interest_rate) ** mortgage_term_in_months
                )
            )
            / ((1 + monthly_interest_rate) ** mortgage_term_in_months - 1),
            2,
        )

    @staticmethod
    def calculate_total_over_loan_term(
        monthly_payment: float, mortgage_term_in_months: int
    ) -> float:
        """
        Calculate the total payment over the loan term.

        Args:
            monthly_payment (float): The monthly payment amount.
            mortgage_term_in_months (int): The mortgage term in months.

        Returns:
            float: The total payment over the loan term.
        """

        return round(monthly_payment * mortgage_term_in_months, 2)

    @staticmethod
    def calculate_total_interest_over_loan_term(
        total_over_loan_term: float, loan_amount: float
    ) -> float:
        """
        Calculate the total interest paid over the loan term.

        Args:
            total_over_loan_term (float): The total payment over the loan term.
            loan_amount (float): The total payment over the loan term.

        Returns:
            float: The total interest paid over the loan term.
        """

        return round(total_over_loan_term - loan_amount, 2)

    @staticmethod
    def calculate_mortgage_term_in_years(mortgage_term: int) -> float:
        """
        Convert mortgage term from months to years.

        Args:
            mortgage_term (int): The mortgage term in months.

        Returns:
            float: The mortgage term in years.
        """

        return mortgage_term / 12
