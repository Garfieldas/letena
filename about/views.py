from django.shortcuts import render
from .models import About_us, Price_table

def about(request):
    about_us = About_us.objects.filter(is_active=True)
    price_table = Price_table.objects.filter(is_active=True)
    context = {'about_us': about_us, 'price_table': price_table}
    return render (request, 'about/us.html', context)
