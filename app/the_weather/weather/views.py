from django.shortcuts import render
import requests


# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=947a289fadf70c93946c0d463998271a'
    city = 'Las Vegas'
    city_weather = requests.get(url.format(city)).json() # Запрос к АПИ и конвертация в  JSON

    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }
    context = {'weather': weather}
    return render(request, 'weather/index.html')
