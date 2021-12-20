from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Level/', views.poziom, name='poziom'),
    path('natlenienie/', views.natlenienie, name='natlenienie'),
    path('schemat/', views.schemat, name='schemat'),
    path('viewChange/', views.viewChange, name='viewChange'),
    path('dateChange/', views.dateChange, name='dateChange'),
    path('data/<str:var1>/minutes/<int:minutes>', views.dane1, name='dane'),
    path('data/<str:var1>/<str:var2>/minutes/<int:minutes>', views.dane2, name='dane'),
    path('data/<str:var1>/<str:var2>/<str:var3>/minutes/<int:minutes>', views.dane3, name='dane'),
    path('gcsv',views.psg),
    path('history/<int:year>/<int:month>',views.history, name='history'),
    path('history/<int:year>/<int:month>/<int:day>',views.history, name='history'),
    path('history/',views.history, name='history')
]