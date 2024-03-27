import pytest
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestLoanViewSet:
    client = APIClient()
    loans_url = "/api/v1/loans/"

    def test_list_loans_empty(self):
        response = self.client.get(self.loans_url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert response.data == []

    def test_list_loans_not_found(self):
        response = self.client.get("/api/v1/loan/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert isinstance(response, HttpResponseNotFound)

    def test_list_loans(self, test_loan_data, test_loan_obj):
        response = self.client.get(self.loans_url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 1

        assert response.data[0]["total_amount"] == test_loan_data["total_amount"]
        assert (
            response.data[0]["total_over_loan_term"]
            == test_loan_data["total_over_loan_term"]
        )
        assert response.data[0]["mortgage_term"] == test_loan_data["mortgage_term"]
        assert response.data[0]["interest_rate"] == test_loan_data["interest_rate"]
        assert response.data[0]["monthly_payment"] == test_loan_data["monthly_payment"]

    def test_generate_rates(self):
        data = {
            "purchase_price": 100000,
            "interest_rate": 5.0,
            "dollar_down_payment": 20000,
            "percentage_down_payment": None,
            "mortgage_term": 30,
        }

        expected_data = {
            "total_amount": 80000.0,
            "monthly_payment": 2842.35,
            "total_over_loan_term": 85270.5,
            "total_interest_paid_over_loan_term": 0.0,
            "mortgage_term_in_years": 2.5,
        }

        response = self.client.post(self.loans_url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(response.data, dict)
        assert len(response.data) != 0

        assert response.data["total_amount"] == expected_data["total_amount"]
        assert (
            response.data["mortgage_term_in_years"]
            == expected_data["mortgage_term_in_years"]
        )
        assert (
            response.data["total_over_loan_term"]
            == expected_data["total_over_loan_term"]
        )
        assert (
            response.data["total_interest_paid_over_loan_term"]
            == expected_data["total_interest_paid_over_loan_term"]
        )
        assert response.data["monthly_payment"] == expected_data["monthly_payment"]

    def test_generate_rates_no_down_payment(self):
        data = {
            "purchase_price": 100000,
            "interest_rate": 5.0,
            "dollar_down_payment": None,
            "percentage_down_payment": None,
            "mortgage_term": 30,
        }

        response = self.client.post(self.loans_url, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(response.data, dict)
        assert len(response.data) != 0

        assert (
            response.data["non_field_errors"][0].title()
            == "Either 'Dollar_Down_Payment' Or 'Percentage_Down_Payment' Must Have A Value."
        )

    def test_generate_rates_bad_request(self):
        data = {
            "purchase_price": None,
            "interest_rate": "invalid number",
            "dollar_down_payment": 10000,
            "percentage_down_payment": "invalid number",
            "mortgage_term": None,
        }

        response = self.client.post(self.loans_url, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(response.data, dict)
        assert len(response.data) != 0

        assert (
            response.data["purchase_price"][0].title() == "This Field May Not Be Null."
        )
        assert (
            response.data["interest_rate"][0].title() == "A Valid Number Is Required."
        )
        assert (
            response.data["percentage_down_payment"][0].title()
            == "A Valid Number Is Required."
        )
        assert (
            response.data["percentage_down_payment"][0].title()
            == "A Valid Number Is Required."
        )
        assert (
            response.data["mortgage_term"][0].title() == "This Field May Not Be Null."
        )
