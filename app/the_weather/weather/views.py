from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm



# Create your views here.

def index(request):
    appid = '947a289fadf70c93946c0d463998271a'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + appid
    cities = City.objects.all()

    err_msg = ''

    message = ''
    message_class = ''

    if request.method == 'POST': # only true if form use
        form = CityForm(request.POST) # add actual request data from poccessing

        if form.is_valid():
            new_city = form.cleaned_data['name']

            existing_city_count = City.objects.filter(name = new_city).count()# filtered repeat name in form
            if existing_city_count == 0:

                city_weather = requests.get(url.format(new_city)).json()
                if city_weather['cod'] == 200: # if answer server 200 OK else err
                    form.save()# save what we add
                else :
                    err_msg = 'Такого города не существует!'
            else :
                err_msg = 'Этот город уже есть в списке '


        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город успешно добавлен в список !'
            message_class = 'is-success'


    form = CityForm()

    weather_data = []

    for city in cities:  #return all cities in database
        city_weather = requests.get(url.format(city)).json() # Запрос к АПИ и конвертация в  JSON
    # print(city_weather.text)


        weather = {
            'city': city.name,
            'temperature': city_weather["main"]["temp"],
            'description': city_weather["weather"][0]["description"],
            'icon': city_weather["weather"][0]["icon"],
        }
        weather_data.append(weather) # add data for current city into our list

    context = {'weather_data': weather_data,
                'form': form,
                'message': message,
                'message_class': message_class
                }
    return render(request, 'weather/index.html', context)



def delete_city(request,city_name):
    City.objects.get(name = city_name).delete()

    return redirect('home')

def delete_everything(request):
    cities = City.objects.all()
    for city in cities:
        City.objects.get(name = city).delete()
    return redirect('home')
