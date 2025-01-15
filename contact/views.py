from django.shortcuts import render, redirect
from .models import Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def contact(request):
    return render(request, 'contact/booking.html')

def submit_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        service = request.POST.get('service')
        email = request.POST.get('email')
        rate = request.POST.get('rate')

        # Create and save the new Review entry
        review = Review.objects.create(name=name, service=service, email=email, rate=rate)
        review.save()
        messages.success(request, 'Ačiū, jūsų atsiliepimas buvo sėkmingai pateiktas!')

        # Redirect to a success page or the same page
        return redirect('review')  # Redirect to a success page or the same form page
    else:
        messages.error(request, 'Visi laukeliai butini!')

    # If GET request, just render the form
    return redirect('review')