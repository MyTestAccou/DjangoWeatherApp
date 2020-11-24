from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


# Create your views here.

def index(request):
    appid = '947a289fadf70c93946c0d463998271a'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + appid
    cities = City.objects.all()

    if request.method == 'POST': # only true if form use
        form = CityForm(request.POST) # add actual request data from poccessing
        form.save() # save what we add

    form = CityForm()

    weather_data = []

    for city in cities:  #return all cities in database
        city_weather = requests.get(url.format(city)).json() # Запрос к АПИ и конвертация в  JSON
    # print(city_weather.text)


        weather = {
            'city': city.name,
            'temperature': city_weather["main"]["temp"],
            'description': city_weather["weather"][0]["description"],
            'icon': city_weather["weather"][0]["icon"]
        }
        weather_data.append(weather) # add data for current city into our list

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)
