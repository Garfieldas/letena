from django.shortcuts import render, redirect
from appointment.models import Appointment
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    today = timezone.now().date()
    current_time = timezone.now().time()
    user_orders = Appointment.objects.filter(client=request.user)
    context = {
        'today': today,
        'current_time': current_time,
        'user_orders': user_orders,  # Assuming you have a queryset of orders
    }
    return render(request, 'dashboard/index.html', context)

def kreipinys(vardas):
    if vardas.endswith('ius'):
        return f'{vardas[:-3]}iau,'  # Pašalina paskutinius 3 simbolius ir prideda „iau“
    elif vardas.endswith('as'):
        return f'{vardas[:-2]}ai,'  # Pašalina paskutinį simbolį ir prideda „au“
    elif vardas.endswith('a'):
        return f'{vardas[:-1]}e,'  # Pašalina paskutinį simbolį ir prideda „e“
    else:
        return f'{vardas},'  # Bendrinis atvejis

def delete(request, pk):
    order = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Jūsų užsakymas buvo panaikintas!')
        email = request.user.email
        vardas = request.user.first_name
        kreipinys_text = kreipinys(vardas)
        client_email = email
        email2 = 'jusuletena@gmail.com'
        phone = '+37067869136'
         #Email
        subject = f'Sveiki, {kreipinys_text} šis laiškas patvirtina jūsų rezervacijos atšaukimą'
        body = (
            f'Jūsų užsakymas nr. {str(pk)[-7:]} yra atšauktas.\n\n\n'
            f'*Dėl papildomų klausimų kreipkitės nurodytais kontaktais: \n'
            f'tel. nr. {phone}.\n'
            f'el. paštas {email2} *'
            )
        #from_email = 'jusuletena@gmail.com'
        # to_email = ['dainiusrainys99@gmail.com']
        from_email = 'jusuletena@gmail.com'
        to_email = [client_email]
        email = EmailMessage(subject, body, from_email, to_email)
        email.send()
        #Second email
         #Email
        subject = f'Sveiki, {str(pk)[-7:]} vizitas yra atšauktas'
        body = (
            f'Jūsų vizitas {str(pk)[-7:]} yra atšauktas.\n\n\n'
            f'Pasitikrinkite administravimo panelę detalesnei informacijai apie kitus užsakymus'
            )
        #from_email = 'jusuletena@gmail.com'
        # to_email = ['dainiusrainys99@gmail.com']
        from_email = 'jusuletena@gmail.com'
        to_email = ['jusuletena@gmail.com']
        email = EmailMessage(subject, body, from_email, to_email)
        email.send()
        #end
        return redirect('home')

    context = {'order':order}
    return render(request, "dashboard/cancel.html", context)
