from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta

from .models import Measurements

from .utils import get_plot

# Create your views here.

def index(request):
    return render(request,"index.html")

def poziom(request):
    time_threshold = datetime.now() - timedelta(hours=1)
    latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold)
    return render(request,"poziom.html", {'latest_measurements_list': latest_measurements_list})

def natlenienie(request):
    time_threshold = datetime.now() - timedelta(minutes=1)
    latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold)
    x = [x.timestamp for x in latest_measurements_list]
    y = [y.natlenienie for y in latest_measurements_list]
    chart = get_plot(x, y, "Wykres natlenienia")

    return render(request,"natlenienie.html", {'latest_measurements_list': latest_measurements_list, 'chart': chart})

def dane(request, variable, minutes):
    possibleVariables = ['natlenienie', 'poziom']
    if variable in possibleVariables:
        time_threshold = datetime.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold)
        toExecute = "[y."+ variable +" for y in latest_measurements_list]"
        x = [x.timestamp for x in latest_measurements_list]
        y = eval(toExecute)
        chart = get_plot(x, y, "Wykres " + variable)
        returnDict = {'latest_measurements_list': latest_measurements_list, 'chart': chart, 'type': variable}
        return render(request,"natlenienie.html", returnDict )
    else:
        return HttpResponseNotFound("Page not found") 

def schemat(request):
    latest_measurements_list = Measurements.objects.latest('id')
    poziom = latest_measurements_list.poziom
    natlenienie = latest_measurements_list.natlenienie
    return render(request,"schemat.html", {'poziom': poziom, 'natlenienie': natlenienie})