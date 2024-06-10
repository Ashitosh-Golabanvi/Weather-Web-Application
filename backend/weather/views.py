from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=35bc2b6acaf37d9db4af0baca705ee25'

   
    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            if not City.objects.filter(name=new_city).exists():
                city_weather = requests.get(url.format(new_city)).json()
                if city_weather.get('cod') == 200:
                    form.save()
                    messages.success(request, f'City {new_city} added successfully!')
                else:
                    messages.error(request, f'City {new_city} not found!')
            else:
                messages.error(request, f'City {new_city} already exists!')
        else:
            messages.error(request, 'Invalid form submission.')
        return redirect('index')  # Redirect to the same view to implement PRG pattern

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()
        if city_weather.get('cod') == 200:
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)