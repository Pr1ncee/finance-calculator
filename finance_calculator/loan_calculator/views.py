from django.db.models import F
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from loan_calculator.models import Loan
from loan_calculator.serializers import (
    LoanInputSerializer,
    LoanOutputSerializer
)
from loan_calculator.services.loan import LoanCalculator


class LoanViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_map = {"list": LoanOutputSerializer, "create": LoanInputSerializer}
    ordering_fields = "__all__"

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, None)

    def get_queryset(self):
        qs = Loan.objects.all()
        return qs.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        response = LoanCalculator.calculate_and_save_loan(
            purchase_price=validated_data["purchase_price"],
            interest_rate=validated_data["interest_rate"],
            dollar_down_payment=validated_data["dollar_down_payment"],
            percentage_down_payment=validated_data["percentage_down_payment"],
            mortgage_term=validated_data["mortgage_term"],
        )
        return Response(response["data"], status=response["status"])
