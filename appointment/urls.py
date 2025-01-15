from django.urls import path
from . import views

urlpatterns  = [
    path('', views.appointment, name='appointment'),
    path('get-booked-times/', views.get_booked_times, name='get_booked_times'),
]