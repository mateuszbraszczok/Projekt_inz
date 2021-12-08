from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Level/', views.poziom, name='poziom'),
    path('natlenienie/', views.natlenienie, name='natlenienie'),
    path('schemat/', views.schemat, name='schemat'),
    path('viewChange/', views.viewChange, name='viewChange'),
    path('dateChange/', views.dateChange, name='dateChange'),
    path('data/<str:variable>/minutes/<int:minutes>', views.dane, name='dane'),
    path('gcsv',views.psg),
    path('history/<int:year>/<int:month>/<int:day>',views.history, name='history'),
    path('history/',views.history, name='history')
]