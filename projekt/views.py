from django.shortcuts import render
from django.http import HttpResponse
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
    print(y)
    print(x)
    chart = get_plot(x, y)

    return render(request,"natlenienie.html", {'latest_measurements_list': latest_measurements_list, 'chart': chart})



def schemat(request):
    latest_measurements_list = Measurements.objects.latest('id')
    poziom = latest_measurements_list.poziom
    print("hi")
    print(poziom)
    natlenienie = latest_measurements_list.natlenienie
    return render(request,"schemat.html", {'poziom': poziom, 'natlenienie': natlenienie})