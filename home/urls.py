from django.urls import path
from . import views

urlpatterns  = [
    path('', views.home, name='home'),
    path('submit_message/', views.submit_message, name='submit_message')
    # path('send_mail_page/', views.send_mail_page, name='send_mail_page')
]