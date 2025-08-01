from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .decorators import user_not_authenticated
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import EmergencyAlert,UserProfile
from django.core.mail import send_mail



# Create your views here.
def core_page(request):
    return render (request,'core_page.html')

@login_required
def settings(request):
    return render (request,'profile/setting.html')

@login_required
def profile(request):
    return render (request,'profile.html')



@user_not_authenticated
def SignUp_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email= form.cleaned_data['email']).exists():
                form.add_error('email','This email is already Registered!')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = "Activte your account."
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https',
                })

                # Generate UID and token
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                # Get domain and scheme
                scheme = request.scheme  # 'http' or 'https'
                domain = get_current_site(request).domain.replace("http://", "").replace("https://", "").strip("/")

                #  Build the activation link
                link = f"{scheme}://{domain}{reverse('activate', kwargs={'uid64': uid, 'token': token})}"
                print("the activateion link. =>", link)


                # Send email
                subject = "Activate your SkillShare account"
                message = f"Hi {user.username},\nPlease click the link below to activate your account:\n\n{link}"

                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject,message,to=[to_email])
                email.send()

                return render(request,'emails/activation_sent.html')
    else:
        form = SignUpForm()


    return render(request,'registration/register.html', {'form': form})

def activate_account(request,uid64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        return render(request,'emails/activation_success.html')
    else:
        return render(request,'emails/activation_invalid.html')


@login_required
def profile_view(request):
    return render(request, 'profile/profile.html', {'user': request.user,})


@login_required
def profile_edit(request):
    # Ensure the user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user')  # or another profile view

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profile/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# password change 
def custom_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password was changed successfully!')
            # return redirect('change')  # your custom success page
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/change_password.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 


# complain function
def complain(request):
    return render (request,'alert/complain.html')


# for alert messages

@login_required
# @csrf_exempt  # Only use this temporarily, for testing!
def emergency_alert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            user = request.user
            profile = UserProfile.objects.get(user=user)

            print("📍 Emergency Location Received:")
            print(f"Latitude: {lat}")
            print(f"Longitude: {lon}")

            if lat and lon:
                EmergencyAlert.objects.create(
                    user=request.user,
                    latitude=lat,
                    longitude=lon,
                    country_name=profile.country_name,
                    phone_number=profile.phone_number,
                    location=profile.location,
                    profile_image=profile.profile_image,
                    # id_photo=profile.id_photo,
                )
                # ✅ Send email
                try:
                    send_mail(
                        subject='🚨 Emergency Alert!',
                        message=f"User: {request.user.username}\nLatitude: {lat}\nLongitude: {lon}",
                        from_email='krishjak1244@gmail.com',
                        recipient_list=['keshavrokaya1244@gmail.com'],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("📧 Email sending failed:", e)
                return JsonResponse({'status': 'success', 'message': 'Alert sent'})
            return JsonResponse({'error': 'Missing coordinates'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=405)


def show_emergency_button(request):
    return render(request, 'alert/alert_button.html')


# the organization one 
@staff_member_required(login_url='/admin/login/')
def emergency_alerts_list(request):
    alerts = EmergencyAlert.objects.all().order_by('-timestamp')
    return render(request, 'alert/emergency_alerts_list.html', {'alerts': alerts})
