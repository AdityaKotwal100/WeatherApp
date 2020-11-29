from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from datetime import datetime
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2a9da8f0ce5b25af4cebee6ea78af333'
    
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name = new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesn't exist! Please add a valid city."
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'
    form = CityForm()


    cities = City.objects.all()
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
        'city' : city.name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'].capitalize(),
        'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)


    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request,'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def weather_forecast(request,city_name):
    url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=2a9da8f0ce5b25af4cebee6ea78af333"
    s = requests.get(url_forecast.format(city_name)).json()
    forecast = []
    lists = s['list']
    for list in lists:
        date_time = list['dt_txt']
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        date = date_time.strftime("%d %B, %Y")
        time = date_time.strftime("%I %p")
        
        city_forecast = {
        'temperature' : list['main']['temp'],
        'max_temperature' : list['main']['temp_max'],
        'min_temperature' : list['main']['temp_min'],
        'feels_like' : list['main']['feels_like'],
        'weather' : list['weather'][0]['main'],
        'icon' : list['weather'][0]['icon'],
        #'timestamp': list['dt_txt'],
        'date': date,
        'time' : time
        }

        forecast.append(city_forecast)
    context = {
        'city_forecast' : forecast,
        'city_name' : city_name
        }
    return render(request,'weather/forecast.html', context)
    



    

    
