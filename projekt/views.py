from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta, date
from dateutil import parser

from django.contrib.auth.decorators import login_required
from .models import Measurements
from register.decorators import allowed_users

from django.utils import timezone

from .utils import *
import csv, math, time
from pythonFiles.variables import *
# Create your views here.

def index(request):
    return render(request,"projekt/index.html")


@login_required(login_url='/login')
@allowed_users(allowed_roles=['authenticated'])
def dane(request, minutes, var1, var2=None, var3=None):
    possibleVariables = tags.copy()
    variables = [var1, var2, var3]
    variables = list(filter(None, variables))

    if any(elem in variables  for elem in tags):
        start = time.time()
        end = time.time()
        print(end - start)

        time_threshold = timezone.now() - timedelta(minutes=minutes)
        latest_measurements_list = Measurements.objects.filter(timestamp__gt=time_threshold).order_by("-id").values('timestamp', *variables)
        start = time.time()
        infoList = getInfoList(variables, latest_measurements_list)

        end = time.time()
        print(end - start)

        start = time.time()
        divisor = math.ceil(minutes/10)
        toExecute1 = "[y1['"+ var1 +"'] for y1 in latest_measurements_list]"
        y1 = eval(toExecute1)
        y1 = y1[::divisor]

        if len(variables) >= 2:
            toExecute2 = "[y2['"+ var2 +"'] for y2 in latest_measurements_list]"
            y2 = eval(toExecute2)
            y2 = y2[::divisor]
        if len(variables) >= 3:
            toExecute3 = "[y3['"+ var3 +"'] for y3 in latest_measurements_list]"
            y3 = eval(toExecute3)
            y3 = y3[::divisor]

        x = [x['timestamp'] for x in latest_measurements_list]
        x = x[::divisor]
        end = time.time()
        print(end - start)

        start = time.time()
        if len(variables) == 1:
            resultList = zip(x, y1)
            chart = get_plot(variables, x, y1)
        if len(variables) == 2:
            resultList = zip(x, y1, y2)
            chart = get_plot(variables, x, y1, y2)
        if len(variables) == 3:
            resultList = zip(x, y1, y2, y3)
            chart = get_plot(variables, x, y1, y2, y3)
        end = time.time()
        print(end - start)

        context = {
            'resultList': resultList, 
            'chart': chart, 
            'type': var1, 
            'possibleVariables': possibleVariables, 
            'minute': minutes, 
            'infoList': infoList,
            'noOfVariables': len(variables),
            'variables': variables
        }
        return render(request, "projekt/data.html", context)
    else:
        return HttpResponseNotFound("Page not found")

def schemat(request):
    latest_measurements_list = Measurements.objects.latest('id')
    context = {
        'latest_measurements_list': latest_measurements_list,  
        'temperaturePercent': ((40.0 - latest_measurements_list.Temperature)/ 25.0) * 100.0 
    }
    return render(request, "projekt/schemat.html", context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['authenticated'])
def viewChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        tagList = list()
        for tag in tags:
            if tag in request.POST:
                tagList.append(str(tag))
        minutes = POSTValues['minutes']

        if len(tagList) == 1:
            returnHtml = "/projekt/minutes/{}/data/{}".format(minutes, tagList[0])
        elif len(tagList) == 2:
            returnHtml = "/projekt/minutes/{}/data/{}/{}".format(minutes, tagList[0], tagList[1])
        elif len(tagList) == 3:
            returnHtml = "/projekt/minutes/{}/data/{}/{}/{}".format(minutes, tagList[0], tagList[1], tagList[2])
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 


@login_required(login_url='/login')
@allowed_users(allowed_roles=['authenticated'])
def history(request, year=None, month=None, day=None):
    if(year ==None or month == None):
        return render(request, "projekt/history.html")

    elif day is not None:
        startdate = date(year, month, day)
        enddate = startdate + timedelta(days=1)
        latest_measurements_list = Measurements.objects.filter(timestamp__range=[startdate, enddate])
        if not latest_measurements_list:
            context = {"noData": True}
            return render(request, "projekt/history.html", context)    
    
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
    elif day is None:
        startdate = date(year, month, 1)
        enddate = date(year + math.floor((month+1)/12), (month+1)%12, 1)
        latest_measurements_list = Measurements.objects.filter(timestamp__range=[startdate, enddate])
        if not latest_measurements_list:
            return render(request, "projekt/history.html", {"noData": True})    

        query="latest_measurements_list.values_list("
        for tag in tags:
            query+='"' +str(tag) + '",'
        query = query[:-1]+")"
        queryset = eval(query)
        response = HttpResponse(content_type='text/csv')
        content = 'attachment; filename="{}-{}.csv"'.format(year, month)
        response['Content-Disposition'] = content
        writer = csv.writer(response, delimiter=";")
        writer.writerow(tags)
        queryset=queryset[::60]
        for line in queryset:
            writer.writerow(line)
    return response

@login_required(login_url='/login')
@allowed_users(allowed_roles=['authenticated'])
def dateChange(request):
    if request.method == 'POST':
        POSTValues = request.POST
        if 'historyDate' in POSTValues:
            dt = parser.parse(POSTValues['historyDate'])
            print(dt)
            returnHtml = "/projekt/history/{}/{}/{}".format(dt.year, dt.month, dt.day)
        elif 'monthDate' in POSTValues:
            dt = parser.parse(POSTValues['monthDate'])
            print(dt)
            returnHtml = "/projekt/history/{}/{}".format(dt.year, dt.month)
            print(returnHtml)
        return redirect(returnHtml)
    else:
        return HttpResponseNotFound("Page not found") 