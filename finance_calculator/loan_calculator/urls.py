from django.urls import include, path
from rest_framework import routers

from loan_calculator import views


app_name = "loan_calculator"

router = routers.DefaultRouter()
router.register(r"loans", views.LoanViewSet, basename="loans")

urlpatterns = [path("", include(router.urls))]

urlpatterns += router.urls
