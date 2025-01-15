from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Carousel, About, Client
from contact.models import Review, Message
from django.contrib import messages
from django.core.mail import EmailMessage

def home(request):
    carousel = Carousel.objects.filter(is_active=True)
    about = About.objects.filter(is_active=True)
    client = Client.objects.filter(is_active=True)
    review = Review.objects.filter(is_active=True)
    context = {'carousel': carousel, 'about': about, 'client': client, 'review': review}
    return render(request, 'home/index.html', context)

def kreipinys(vardas):
    if vardas.endswith('ius'):
        return f'{vardas[:-3]}iau,'  # Pašalina paskutinius 3 simbolius ir prideda „iau“
    elif vardas.endswith('as'):
        return f'{vardas[:-2]}ai,'  # Pašalina paskutinį simbolį ir prideda „au“
    elif vardas.endswith('a'):
        return f'{vardas[:-1]}e,'  # Pašalina paskutinį simbolį ir prideda „e“
    else:
        return f'{vardas},'  # Bendrinis atvejis

def submit_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        client_email = email
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        #Email
        subject = f'Gauta žinutė iš vartotojo {name}'
        body = message + '\n\n\n' + f'\n*Pranešėjo kontaktai: \n tel.nr {phone}.\n el.paštas {email} *'
        #from_email = 'jusuletena@gmail.com'
        # to_email = ['dainiusrainys99@gmail.com']
        from_email = 'jusuletena@gmail.com'
        to_email = ['jusuletena@gmail.com']
        email = EmailMessage(subject, body, from_email, to_email)
        email.send()

        #End
        kreipinys_text = kreipinys(name)
        email2 = 'jusuletena@gmail.com'
        tel_nr = '+37067869136'
        #Email
        subject = f'Sveiki, {kreipinys_text} jūsų pranešimas gautas'
        body = (
            f'Jūsų žinutė gauta, ir mes susisieksime su jumis per 24 valandas. \n\n\n'
            f'Jūsų pranešimas: \n'
            f'* {message}. *\n'
            f'Mūsų tiesioginiai kontaktai: \n'
            f'el.paštas: {email2} \n'
            f'tel nr: {tel_nr}'
            )
        from_email = email2
        to_email = [client_email]
        email = EmailMessage(subject, body, from_email, to_email)
        email.send()
        #End

        message = Message.objects.create(name=name, email=email, phone=phone, message=message)
        message.save()
        messages.success(request, 'Ačiū, jūsų žinutė buvo išsiųsta sėkmingai!')

        # Redirect to a success page or the same page
        return redirect('home')  # Redirect to a success page or the same form page
    else:
        messages.error(request, 'Visi laukeliai būtini!')

    # If GET request, just render the form
    return redirect('home')
