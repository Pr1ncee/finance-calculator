from django.urls import include, path
from rest_framework import routers

routers = routers.DefaultRouter()

urlpatterns = [
    path("api/v1/", include("loan_calculator.urls")),
]

urlpatterns += routers.urls
