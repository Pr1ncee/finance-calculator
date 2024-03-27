from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from loan_calculator.models import Loan


class LoanOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class LoanInputSerializer(serializers.Serializer):
    purchase_price = serializers.FloatField(validators=[MinValueValidator(0)])
    interest_rate = serializers.FloatField(validators=[MinValueValidator(0)])
    dollar_down_payment = serializers.FloatField(
        allow_null=True, validators=[MinValueValidator(0)]
    )
    percentage_down_payment = serializers.FloatField(
        allow_null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    mortgage_term = serializers.IntegerField(validators=[MinValueValidator(0)])

    def validate(self, data):
        dollar_down_payment = data.get("dollar_down_payment")
        percentage_down_payment = data.get("percentage_down_payment")

        # Check if exactly one of dollar_down_payment or percentage_down_payment is null
        if not any([dollar_down_payment, percentage_down_payment]):
            raise serializers.ValidationError(
                "Either 'dollar_down_payment' or 'percentage_down_payment' must have a value."
            )
        return data
