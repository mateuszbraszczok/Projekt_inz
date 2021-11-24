from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poziom/', views.poziom, name='poziom'),
    path('natlenienie/', views.natlenienie, name='natlenienie'),
    path('schemat/', views.schemat, name='schemat'),
    path('viewChange/', views.viewChange, name='viewChange'),
    path('data/<str:variable>/minutes/<int:minutes>', views.dane, name='dane'),
]