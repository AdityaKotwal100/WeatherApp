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
            #Maintains a count of cities to check if City has been added before
            existing_city_count = City.objects.filter(name = new_city).count()

            #If city isn't added, save city.
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                #If API returns correct response (i.e. entered city exists in the world), save the city.
                if r['cod'] == 200:
                    form.save()
                #If API doesn't return correct response, Give warning.
                else:
                    err_msg = "City doesn't exist! Please add a valid city."
            #If city is added, give warning.
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

        #Data to be sent to front end.
        city_weather = {
        'city' : city.name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'].capitalize(),
        'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    #Data to be sent to front end.
    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request,'weather/weather.html', context)

#Deletes selected city from home page.
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

#Fetches next 5 day forecast for selected city.
def weather_forecast(request,city_name):
    url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=2a9da8f0ce5b25af4cebee6ea78af333"
    s = requests.get(url_forecast.format(city_name)).json()
    forecast = []
    #Fetching information from JSON object.
    lists = s['list']
    for list in lists:
        date_time = list['dt_txt']
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        date = date_time.strftime("%d %B, %Y")
        time = date_time.strftime("%I %p")
        
        #All information needed to display
        city_forecast = {
        'temperature' : list['main']['temp'],
        'max_temperature' : list['main']['temp_max'],
        'min_temperature' : list['main']['temp_min'],
        'feels_like' : list['main']['feels_like'],
        'weather' : list['weather'][0]['main'],
        'icon' : list['weather'][0]['icon'],
        'date': date,
        'time' : time
        }

        forecast.append(city_forecast)

        #Context to be rendered in the front end.
    context = {
        'city_forecast' : forecast,
        'city_name' : city_name
        }
    return render(request,'weather/forecast.html', context)
    



    

    
