from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurements

# Create your views here.

def index(request):
    return render(request,"index.html")

def poziom(request):
    # output = "<h1> poziom pomiary </h1>"
    latest_measurements_list = Measurements.objects.order_by('-timestamp')[:10]
    print(latest_measurements_list)
    # output += ',</br> '.join([ "{}     <b>{:.3f}</b>".format(str(q.timestamp),float(q.poziom))   for q in latest_measurements_list])
    # return HttpResponse(output)
    return render(request,"poziom.html", {'latest_measurements_list': latest_measurements_list})

def natlenienie(request):
    latest_measurements_list = Measurements.objects.order_by('-timestamp')[:10]
    output = "<h1> natlenienie pomiary </h1>"
    output += ',</br> '.join([ "{}     <b>{:.3f}</b>".format(str(q.timestamp),float(q.natlenienie))   for q in latest_measurements_list])
    return HttpResponse(output)