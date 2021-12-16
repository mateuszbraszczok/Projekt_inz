from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta, date
from dateutil import parser
from django.db.models import Avg, Max, Min
from django.contrib.auth.decorators import login_required
from .models import Measurements

from django.utils import timezone

from .utils import get_plot
import csv
from pythonFiles.variables import tags
# Create your views here.

def index(request):
    return render(request,"projekt/index.html")

@login_required(login_url='/login')
def poziom(request):
    time_threshold = datetime.now() - timedelta(hours=1)
    latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold)
    return render(request,"projekt/poziom.html", {'latest_measurements_list': latest_measurements_list})

def natlenienie(request):
    time_threshold = datetime.now() - timedelta(minutes=1)
    latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold)
    x = [x.timestamp for x in latest_measurements_list]
    y = [y.natlenienie for y in latest_measurements_list]
    chart = get_plot(x, y, "Wykres natlenienia")

    return render(request,"projekt/natlenienie.html", {'latest_measurements_list': latest_measurements_list, 'chart': chart})

@login_required(login_url='/login')    
def dane1(request, var1, minutes):
    # letter_list = var1.split(",")
    # print(letter_list)
    possibleVariables = tags.copy()

    if var1 in tags:
        #possibleVariables.remove(var1)
        time_threshold = timezone.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold).order_by("-id")
        infoList = latest_measurements_list.aggregate(Avg(var1), Max(var1), Min(var1))
        toExecute = "[y."+ var1 +" for y in latest_measurements_list]"
        x = [x.timestamp for x in latest_measurements_list]
        y = eval(toExecute)
        resultList = zip(x, y)
        variables = [var1]
        chart = get_plot(variables, x, y)
        
        
        returnDict = {'resultList': resultList, 'chart': chart, 'type': var1, 'possibleVariables': possibleVariables, 'minute': minutes, 'infoList': infoList,
            'noOfVariables': 1,
            'variables': variables}
        return render(request, "projekt/data.html", returnDict )
    else:
        return HttpResponseNotFound("Page not found") 

@login_required(login_url='/login')
def dane2(request, var1, var2, minutes):
    # letter_list = var1.split(",")
    # print(letter_list)
    possibleVariables = tags.copy()

    if var1 in tags:
        #possibleVariables.remove(var1)
        time_threshold = timezone.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold).order_by("-id")
        infoList = latest_measurements_list.aggregate(Avg(var1), Max(var1), Min(var1))
        toExecute1 = "[y1."+ var1 +" for y1 in latest_measurements_list]"
        toExecute2 = "[y2."+ var2 +" for y2 in latest_measurements_list]"
        x = [x.timestamp for x in latest_measurements_list]
        y1 = eval(toExecute1)
        y2 = eval(toExecute2)
        resultList = zip(x, y1, y2)

        variables = [var1, var2]
        chart = get_plot(variables, x, y1, y2)
            
        returnDict = {'resultList': resultList, 
            'chart': chart, 
            'type': var1, 
            'possibleVariables': possibleVariables, 
            'minute': minutes, 
            'infoList': infoList,
            'noOfVariables': 2,
            'variables': variables }
        return render(request, "projekt/data.html", returnDict )
    else:
        return HttpResponseNotFound("Page not found") 

@login_required(login_url='/login')
def dane3(request, var1, var2, var3, minutes):
    # letter_list = var1.split(",")
    # print(letter_list)
    possibleVariables = tags.copy()
    
    if var1 in tags:
        #possibleVariables.remove(var1)
        time_threshold = timezone.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold).order_by("-id")
        infoList = latest_measurements_list.aggregate(Avg(var1), Max(var1), Min(var1))
        toExecute1 = "[y1."+ var1 +" for y1 in latest_measurements_list]"
        toExecute2 = "[y2."+ var2 +" for y2 in latest_measurements_list]"
        toExecute3 = "[y3."+ var3 +" for y3 in latest_measurements_list]"
        x = [x.timestamp for x in latest_measurements_list]
        y1 = eval(toExecute1)
        y2 = eval(toExecute2)
        y3 = eval(toExecute3)
        if minutes > 60:
            x = x[::10]
            y1 = y1[::10]
            y2 = y2[::10]
            y3 = y3[::10]
        elif minutes > 30:
            x = x[::2]
            y1 = y1[::2]
            y2 = y2[::2]
            y3 = y3[::2]

        resultList = zip(x, y1, y2, y3)
        

        variables = [var1, var2, var3]
        chart = get_plot(variables, x, y1, y2, y3)
        returnDict = {'resultList': resultList, 
            'chart': chart, 
            'type': var1, 
            'possibleVariables': possibleVariables, 
            'minute': minutes, 
            'infoList': infoList,
            'noOfVariables': 3,
            'variables': variables}
        return render(request, "projekt/data.html", returnDict )
    else:
        return HttpResponseNotFound("Page not found") 

def schemat(request):
    latest_measurements_list = Measurements.objects.latest('id')
    level = latest_measurements_list.Level
    temperaturePercent = dict()
    temperaturePercent["temperaturePercent"] = ((40.0 - latest_measurements_list.Temperature)/ 25.0) *100.0
    return render(request,"projekt/schemat.html", {'level': level, 'latest_measurements_list': latest_measurements_list, "temperaturePercent":temperaturePercent})

@login_required(login_url='/login')
def viewChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        tagList = list()
        for tag in tags:
            if tag in request.POST:
                tagList.append(str(tag))

        if len(tagList) == 1:
            returnHtml = "/projekt/data/{}/minutes/{}".format(tagList[0], POSTValues['minutes'])
        elif len(tagList) == 2:
            returnHtml = "/projekt/data/{}/{}/minutes/{}".format(tagList[0], tagList[1], POSTValues['minutes'])
        elif len(tagList) == 3:
            returnHtml = "/projekt/data/{}/{}/{}/minutes/{}".format(tagList[0], tagList[1], tagList[2], POSTValues['minutes'])
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 


@login_required(login_url='/login')
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

@login_required(login_url='/login')
def history(request, year=None, month=None, day=None):
    if(year ==None or month == None or day == None):
        latest_measurements_list = Measurements.objects.filter(timestamp__gte = date.today())
        return render(request, "projekt/history.html" )

    else:
        startdate = date(year, month, day)
        enddate = startdate + timedelta(days=1)
        latest_measurements_list = Measurements.objects.filter(timestamp__range=[startdate, enddate])
        if not latest_measurements_list:
            return render(request, "projekt/history.html", {"noData": True} )    
    
    #response = psg(request, latest_measurements_list)


        query="latest_measurements_list.values_list("
        for tag in tags:
            query+='"' +str(tag) + '",'
        query = query[:-1]+")"
        queryset = eval(query)
        response = HttpResponse(content_type='text/csv')
        content = 'attachment; filename="{}-{}-{}.csv"'.format(year, month, day)
        response['Content-Disposition'] = content
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

@login_required(login_url='/login')
def dateChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        dt = parser.parse(POSTValues['historyDate'])
        print(dt)
        returnHtml = "/projekt/history/{}/{}/{}".format(dt.year, dt.month, dt.day)
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 