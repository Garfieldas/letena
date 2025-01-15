from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.signing import Signer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.signing import BadSignature, Signer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login as auth_login, authenticate, logout
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

def register(request):
    if request.method == 'POST':
        name = request.POST.get('vardas')
        surname = request.POST.get('pavarde')
        username = request.POST.get('prisijungimo_vardas')
        email = request.POST.get('el_pastas')
        password = request.POST.get('slaptazodis')

        # Get CAPTCHA values from the form
        captcha_key = request.POST.get('captcha_key')
        captcha_response = request.POST.get('captcha_response')

        try:
            # Validate the CAPTCHA
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response != captcha_response.lower():  # Case-insensitive comparison
                messages.error(request, 'CAPTCHA įvesta neteisingai, bandykite dar kartą.')
                # Generate a new CAPTCHA if the current one is incorrect
                captcha_key = CaptchaStore.generate_key()
                captcha_image_url_path = captcha_image_url(captcha_key)
            else:
                # Check if the username or email is already taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Vartotojas su šio prisijungimo vardu jau egzistuoja!')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Šis el.paštas jau užimtas!')
                else:
                    # Create the user if all checks pass
                    user = User.objects.create_user(
                        first_name=name,
                        last_name=surname,
                        username=username,
                        email=email,
                        password=password,
                        is_active=False  # Initially, the user is inactive
                    )

                    # Generate a token for email verification
                    signer = Signer()  # A Django utility to create signatures
                    token = signer.sign(user.pk)  # Sign the user's ID

                    # Build the verification URL
                    verification_url = request.build_absolute_uri(
                        reverse('verify_email', args=[urlsafe_base64_encode(force_bytes(user.pk)), token])
                    )

                    # Send email verification
                    subject = 'Patvirtinkite savo el.paštą'
                    message = (f'Sveiki {name},\n\nPrašau paspauskite ant šios nuorodos žemiau, '
                               f'kad patvirtintumėte savo el.pašto adresą ir užbaigtumėte registraciją:\n\n'
                               f'{verification_url}\n\nAčiū!')
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

                    messages.success(request, 'Registracija sėkminga! Patikrinkite savo el.paštą, kad aktyvuotumėte paskyrą.')
                    return redirect('home')  # Redirect to the home page after successful registration

        except CaptchaStore.DoesNotExist:
            messages.error(request, 'Neteisinga CAPTCHA, bandykite dar kartą.')
            # Generate a new CAPTCHA if the current one does not exist
            captcha_key = CaptchaStore.generate_key()
            captcha_image_url_path = captcha_image_url(captcha_key)
    else:
        # Generate a new CAPTCHA for the GET request
        captcha_key = CaptchaStore.generate_key()
        captcha_image_url_path = captcha_image_url(captcha_key)

    return render(request, 'accounts/register.html', {
        'captcha_key': captcha_key,
        'captcha_image_url': captcha_image_url_path,
        'vardas': request.POST.get('vardas', ''),
        'pavarde': request.POST.get('pavarde', ''),
        'prisijungimo_vardas': request.POST.get('prisijungimo_vardas', ''),
        'el_pastas': request.POST.get('el_pastas', ''),
    })





def verify_email(request, uidb64, token):
    try:
        # Decode the user's ID and verify the signature
        user_id = urlsafe_base64_decode(uidb64).decode()
        signer = Signer()
        signer.unsign(token)  # Check if the token is valid

        user = User.objects.get(pk=user_id)
        if not user.is_active:
            user.is_active = True  # Activate the user
            user.save()
            messages.success(request, 'Jūsu paskyra patvirtinta, galite prisijungti.')
            return redirect('home')
        else:
            messages.warning(request, 'Jūsu paskyra jau buvo patvirtinta.')
    except (User.DoesNotExist, BadSignature):
        messages.error(request, 'Negalima patvirtinimo nuoroda.')

    return redirect('register')

def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home page if the user is already logged in

    if request.method == 'POST':
        username = request.POST.get('prisijungimo_vardas')
        password = request.POST.get('slaptazodis')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            messages.success(request, 'Jūs sėkmingai prisijungiate!')
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Neteisingi prisijungimo duomenys, bandykite dar kartą.')

    # Render the login page for GET requests or if login failed
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Jūs sėkmingai atsijungiate!')
    return redirect('home')


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            signer = Signer()
            token = signer.sign(user.pk)  # Sign the user's ID
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the reset password URL
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[uidb64, token])
            )

            # Send the reset password email
            subject = 'Slaptažodžio atstatymas'
            message = (f'Sveiki,\n\nNorėdami atstatyti slaptažodį, paspauskite žemiau esančią nuorodą:\n\n'
                       f'{reset_url}\n\nJeigu gavote šį laišką per klaidą ignoruokite\n\nAčiū!')
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, 'Slaptažodžio atsatymo nuoroda išsiųstą į jūsų el.paštą.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Paskyros su šio el.paštum neegzistuoja.')

    return render(request, 'accounts/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        signer = Signer()
        signer.unsign(token)  # Check if the token is valid

        user = User.objects.get(pk=user_id)

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Jūsų slaptažodis atstatytas sėkmingai.')
                return redirect('login')
            else:
                messages.error(request, 'Slaptažodžiai nesutampa. Pabandykite dar kartą.')

        return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
    except (User.DoesNotExist, BadSignature):
        messages.error(request, 'Slaptažodžio atstatymo nuoroda jau nebegalioja.')
        return render(request, 'accounts/password_reset_confirm.html', {'validlink': False})
