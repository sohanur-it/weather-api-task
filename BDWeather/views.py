import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import District
from datetime import timedelta
from django.utils import timezone
from .models import DistTemp
from . import responses

from rest_framework.views import APIView

from .models import DistTemp
from django.db.models import Avg
from datetime import datetime


class CoolestDistrict(APIView):
    def get(self, request):
        # Get the average temperatures for all districts, ordered by average temperature
        average_temps = DistTemp.objects.values('district__name').annotate(average_temp=Avg('temp')).order_by('average_temp')

        # Select the lowest 10 entries
        lowest_10_temps = average_temps[:10]

        # Prepare a dictionary to store the results
        lowest_temps_per_district = {}
        for data in lowest_10_temps:
            district_name = data['district__name']
            average_temp = round(data['average_temp'], 2)  # Round to two decimal places
            lowest_temps_per_district[district_name] = average_temp

        return responses.success(lowest_temps_per_district)

'''
# payload

{
    "current_location":"Dhaka",
    "destination": "Thakurgaon",
    "date": "2024-02-14"
}

'''


class CheckLocation(APIView):
    def post(self, request):
        # Extract data from request
        current_location = request.data.get('current_location')
        destination = request.data.get('destination')
        date_str = request.data.get('date')

        # Convert date string to datetime object
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Fetch temperature information for current location and destination
        source_temp = DistTemp.objects.filter(district__name=current_location, date_time__date=date_object).first()
        destination_temp = DistTemp.objects.filter(district__name=destination, date_time__date=date_object).first()

        # Determine decision based on temperature comparison
        if source_temp is None:
            return responses.error(
                {'error': 'Temperature data not available for the current location on the specified date'})

        if destination_temp is None:
            return responses.error({'error': 'Temperature data not available for the destination on the specified date'})

        if source_temp.temp > destination_temp.temp:
            remarks = 'Source temperature is higher than destination temperature.'
            decision = 'Travel'
        else:
            remarks = 'Source temperature is less than destination temperature.'
            decision = 'Postpone'

        # Prepare response
        res = {
            'source_temp': source_temp.temp,
            'destination_temp': destination_temp.temp,
            'remarks': remarks,
            'decision': decision
        }

        return responses.success(res)


@api_view(['GET'])
def fetch_lat_long(request):
    districts_url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    response = requests.get(districts_url)

    if response.status_code == 200:
        data = response.json()
        districts = data['districts']

        district_info = [(district['lat'], district['long'], district['name']) for district in districts]
        print(district_info)

        return responses.success('saved in db')


def fetch_forecast_for_district(latitude, longitude):
    base_url = "https://api.open-meteo.com/v1/forecast"
    today = timezone.now().date()
    end_date = today + timedelta(days=7)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "hourly": "temperature_2m",
        "timezone": "Asia/Dhaka",
        "format": "json",
        "timeformat": "iso8601",
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def coolest_districts(request):
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
    return responses.success({"message": "Forecasts saved to the database."})


@api_view(['GET'])
def get_district(request):
    target_url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
    response = requests.get(target_url)
    data = response.json()['districts']
    for district in data:
        dist_name = district['name']
        lat = district['lat']
        long = district['long']
        District.objects.get_or_create(name=dist_name, lat=lat, long=long)
    return responses.success(data)
