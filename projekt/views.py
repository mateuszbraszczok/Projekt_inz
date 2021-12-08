from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta, date
from dateutil import parser
from django.db.models import Avg, Max, Min
from .models import Measurements

from django.utils import timezone

from .utils import get_plot
import csv
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
    level = latest_measurements_list.Level
    oxygen = latest_measurements_list.Oxygen
    substrate = latest_measurements_list.Substrate
    return render(request,"schemat.html", {'level': level, 'oxygen': oxygen, 'substrate': substrate, 'latest_measurements_list': latest_measurements_list})

def viewChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        returnHtml = "/projekt/data/{}/minutes/{}".format(POSTValues['variable'], POSTValues['minutes'])
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 


def psg(request, date):
    query="date.values_list("
    for tag in tags:
        query+='"' +str(tag) + '",'
    query = query[:-1]+")"
    queryset = eval(query)
    print("response")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    writer = csv.writer(response, delimiter=";")
    writer.writerow(tags)
    print(queryset)
    for user in queryset:
        print(user)
        writer.writerow(user)
    
    return response

def history(request, year=None, month=None, day=None):
    if(year ==None or month == None or day == None):
        latest_measurements_list = Measurements.objects.filter(timestamp__gte = date.today())
        return render(request,"history.html" )

    else:
        startdate = date(year, month, day)
        enddate = startdate + timedelta(days=1)
        latest_measurements_list = Measurements.objects.filter(timestamp__range=[startdate, enddate])
        if not latest_measurements_list:
            return render(request,"history.html", {"noData": True} )    
    
    #response = psg(request, latest_measurements_list)


        query="latest_measurements_list.values_list("
        for tag in tags:
            query+='"' +str(tag) + '",'
        query = query[:-1]+")"
        queryset = eval(query)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response, delimiter=";")
        writer.writerow(tags)
        for user in queryset:
            writer.writerow(user)

    #print(latest_measurements_list)
    # statsList=list()
    # for tag in tags:
    #     if tag == "timestamp":
    #         continue
    #     infoList = latest_measurements_list.aggregate(Avg(tag), Max(tag), Min(tag))
    #     statsList.append(infoList)
    # #print(statsList)
    # returnDict = {'statsList' :statsList}
    # return render(request,"history.html", {'returnDict': returnDict})
    return response

def dateChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        dt = parser.parse(POSTValues['historyDate'])
        print(dt)
        returnHtml = "/projekt/history/{}/{}/{}".format(dt.year, dt.month, dt.day)
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 