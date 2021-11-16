from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poziom/', views.poziom, name='poziom'),
    path('natlenienie/', views.natlenienie, name='natlenienie'),
]