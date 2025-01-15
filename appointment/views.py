from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def kreipinys(vardas):
    if vardas.endswith('ius'):
        return f'{vardas[:-3]}iau,'  # Pašalina paskutinius 3 simbolius ir prideda „iau“
    elif vardas.endswith('as'):
        return f'{vardas[:-1]}au,'  # Pašalina paskutinį simbolį ir prideda „au“
    elif vardas.endswith('a'):
        return f'{vardas[:-1]}e,'  # Pašalina paskutinį simbolį ir prideda „e“
    else:
        return f'{vardas},'  # Bendrinis atvejis

@login_required
def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.client_email = request.user.email
            vardas = request.user.first_name
            kreipinys_text = kreipinys(vardas)
            appointment.save()
           # name = request.POST.get('appointment.client')
            email = request.user.email
            client_email = email
            phone = request.POST.get('client_phone')
            day = request.POST.get('day')
            time = request.POST.get('time')
            #Email
            subject = f'Gauta žinutė iš vartotojo {vardas} dėl rezervacijos'
            body = f'Gautą informaciją apie nauja klientą,kuris ketina apsilankyti {day} diena' + f'\n {time} val.' +  '\n\n\n'  + f'\n*Pranešėjo kontaktai: \n tel.nr {phone}.\n el.paštas {email} *'
            #from_email = 'jusuletena@gmail.com'
            # to_email = ['dainiusrainys99@gmail.com']
            from_email = 'jusuletena@gmail.com'
            to_email = ['jusuletena@gmail.com']
            email = EmailMessage(subject, body, from_email, to_email)
            email.send()
        #End
        #Second email to User
            subject = f'Sveiki {kreipinys_text} patvirtinimas apie jūsų rezervaciją'
            phone = '+37067869136'
            email2 = 'jusuletena@gmail.com'
            to_email = [client_email]
            body = f'Gautą informaciją apie jūsų vizitą,kuris vyks {day} diena' + f'\n {time} val.' +  '\n\n\n'  + f'\n*Kontaktai dėl iškilusių klausimų: \n tel.nr {phone}.\n el.paštas {email2} *'
            email = EmailMessage(subject, body, from_email, to_email)
            email.send()

            form.save()
            messages.success(request, 'Jūsų rezervacija sekmingai patvirtinta')
            return redirect('home')
    else:
        form = AppointmentForm()
    context = {'form': form}
    return render(request, 'appointment/index2.html', context)



def get_booked_times(request):
    date = request.GET.get('date')
    if date:
        # Fetch all the booked times for the given date from the Appointment model
        booked_times = Appointment.objects.filter(day=date).values_list('time', flat=True)
        # Convert the time values to a string format like 'HH:MM' to match the dropdown options
        booked_times = [time.strftime('%H:%M') for time in booked_times]
        return JsonResponse(booked_times, safe=False)
    else:
        return JsonResponse([], safe=False)
