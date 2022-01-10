from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schemat/', views.schemat, name='schemat'),
    path('minutes/<int:minutes>/data/<str:var1>/', views.dane, name='dane1'),
    path('minutes/<int:minutes>/data/<str:var1>/<str:var2>/', views.dane, name='dane2'),
    path('minutes/<int:minutes>/data/<str:var1>/<str:var2>/<str:var3>/', views.dane, name='dane3'),
    path('history/<int:year>/<int:month>/', views.history, name='historyMonth'),
    path('history/<int:year>/<int:month>/<int:day>/', views.history, name='historyDay'),
    path('history/', views.history, name='history'),
    path('viewChange/', views.viewChange, name='viewChange'),
    path('dateChange/', views.dateChange, name='dateChange')
]