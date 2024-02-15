from __future__ import absolute_import
from celery import shared_task
from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

import sys
import logging
import datetime
import requests
from .models import District
from .views import fetch_forecast_for_district
from .models import DistTemp

@shared_task
def fetch_district():
    print("run from celery beat ....")
    target_url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    response = requests.get(target_url)
    data = response.json()['districts']
    for district in data:
        dist_name = district['name']
        lat = district['lat']
        long = district['long']
        District.objects.get_or_create(name=dist_name, lat=lat, long=long)

    print('save districts in database')



@shared_task
def fetch_temp_each_dist():
    districts = District.objects.all()
    for district in districts:
        forecasts = fetch_forecast_for_district(district.lat, district.long)
        if forecasts:
            data = forecasts['hourly']
            filtered_temperatures = [(time, temp) for time, temp in zip(data['time'], data['temperature_2m']) if
                                     time.endswith('T14:00')]
            for time, temperature in filtered_temperatures:
                dist_obj, _ = District.objects.get_or_create(name=district.name, lat=district.lat, long=district.long)
                DistTemp.objects.get_or_create(district=dist_obj, date_time=time, temp=temperature)
                print(f"Time: {time}, Temperature: {temperature}, District: {district.name}")
    print('forecasts save to db')
