from django.shortcuts import render
import requests
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2a9da8f0ce5b25af4cebee6ea78af333'
    city = 'Las Vegas'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon ' : r['weather'][0]['icon'],

    }

    context = {'city_weather' : city_weather}
    return render(request,'weather/weather.html', context)