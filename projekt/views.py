from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta
from django.db.models import Avg, Max, Min
from .models import Measurements

from django.utils import timezone

from .utils import get_plot

from pythonFiles.variables import tags
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
    possibleVariables = tags.copy()

    if variable in tags:
        possibleVariables.remove(variable)
        time_threshold = timezone.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold).order_by("-id")
        infoList = latest_measurements_list.aggregate(Avg(variable), Max(variable), Min(variable))
        toExecute = "[y."+ variable +" for y in latest_measurements_list]"
        x = [x.timestamp for x in latest_measurements_list]
        y = eval(toExecute)
        resultList = zip(x,y)
        chart = get_plot(x, y, variable)
        
        returnDict = {'resultList': resultList, 'chart': chart, 'type': variable, 'possibleVariables': possibleVariables, 'minute': minutes, 'infoList': infoList}
        return render(request,"data.html", returnDict )
    else:
        return HttpResponseNotFound("Page not found") 

def schemat(request):
    latest_measurements_list = Measurements.objects.latest('id')
    poziom = latest_measurements_list.Level
    natlenienie = latest_measurements_list.Oxygen
    print("render")
    return render(request,"schemat.html", {'poziom': poziom, 'natlenienie': natlenienie})

def viewChange(request):
    if request.method == 'POST':
        print("\n\nhi\n")
        POSTValues = request.POST

        print(POSTValues['variable'])
        print(POSTValues['minutes'])
        html=""
        returnHtml = "/projekt/data/{}/minutes/{}".format(POSTValues['variable'], POSTValues['minutes'])
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 
    # latest_measurements_list = Measurements.objects.latest('id')
    # poziom = latest_measurements_list.poziom
    # natlenienie = latest_measurements_list.natlenienie
    # return render(request,"schemat.html", {'poziom': poziom, 'natlenienie': natlenienie})