from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('find-coolest-district/', CoolestDistrict.as_view()),
    path('check-location/', CheckLocation.as_view()),
    # path('get_district/', get_district),
    # path('fetch_forecasts/', coolest_districts),
]