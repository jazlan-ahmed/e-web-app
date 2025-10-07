from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import (CustomUserCreationForm, VerifyCodeForm, UserAddress, location_data, 
                   ForgotPasswordForm, VerifyResetCodeForm, SetNewPasswordForm)
from .models import Address, Profile
import random
import time


# Authentication views
class UserLoginView(LoginView):
    template_name = 'login.html'

user_login = UserLoginView.as_view()


class UserLogoutView(LogoutView):
    next_page = 'login'

user_logout = UserLogoutView.as_view()


def user_registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Prepare verification code
            code = f"{random.randint(100000, 999999)}"
            # Hash password and store minimal data in session until verification
            hashed_password = make_password(form.cleaned_data['password1'])
            pending = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'account_type': form.cleaned_data['account_type'],
                'hashed_password': hashed_password,
                'code': code,
            }
            request.session['pending_registration'] = pending
            # Send email if configured
            try:
                send_mail(
                    subject='Your verification code',
                    message=f'Your verification code is: {code}',
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[pending['email']],
                    fail_silently=not settings.DEBUG,
                )
            except Exception:
                pass
            return redirect('verify')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def verify_registration_code(request):
    pending = request.session.get('pending_registration')
    if not pending:
        messages.error(request, 'No pending registration found. Please register again.')
        return redirect('register')
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == pending['code']:
                # Create user
                user = User(username=pending['username'], email=pending['email'], password=pending['hashed_password'])
                user.save()
                Profile.objects.create(user=user, account_type=pending['account_type'])
                auth_login(request, user)
                # clear session
                try:
                    del request.session['pending_registration']
                except KeyError:
                    pass
                return redirect('home')
            else:
                messages.error(request, 'Invalid code. Please try again.')
    else:
        form = VerifyCodeForm()
    return render(request, 'register_verify.html', {'form': form, 'email': pending.get('email')})


def resend_verification_code(request):
    from django.http import JsonResponse
    import json
    import time
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    pending = request.session.get('pending_registration')
    if not pending:
        return JsonResponse({'error': 'No pending registration found'}, status=400)
    
    # Check if user is requesting too frequently (rate limiting)
    last_resend = request.session.get('last_resend_time', 0)
    current_time = time.time()
    if current_time - last_resend < 60:  # 60 second cooldown
        remaining = 60 - (current_time - last_resend)
        return JsonResponse({'error': f'Please wait {int(remaining)} more seconds'}, status=429)
    
    # Generate new code
    code = f"{random.randint(100000, 999999)}"
    pending['code'] = code
    request.session['pending_registration'] = pending
    request.session['last_resend_time'] = current_time
    
    # Send email
    try:
        send_mail(
            subject='Your new verification code',
            message=f'Your new verification code is: {code}',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[pending['email']],
            fail_silently=not settings.DEBUG,
        )
        return JsonResponse({'success': True, 'message': 'New code sent successfully'})
    except Exception as e:
        return JsonResponse({'error': 'Failed to send email'}, status=500)


# Address and location helpers
from django.http import JsonResponse

def load_states(request):
    country = request.GET.get("country")
    states = list(location_data.get(country, {}).keys())
    return JsonResponse({"states": states})

def load_cities(request):
    country = request.GET.get("country")
    state = request.GET.get("state")
    cities = location_data.get(country, {}).get(state, [])
    return JsonResponse({"cities": cities})

def add_address(request):
    if request.method == "POST":
        form = UserAddress(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Address.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                mobile=data["mobile"],
                pincode=data["pincode"],
                address=data["address"],
                country=data["country"],
                state=data["state"],
                city=data["city"],
                landmark=data.get("landmark"),
                alternative_mobile=data.get("alternative_mobile"),
            )
            return redirect("index")  # redirect to homepage or checkout
    else:
        form = UserAddress()

    return render(request, "users/address_form.html", {"form": form})


@login_required(login_url='login')
def seller_dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.account_type != 'seller':
        return redirect('home')
    return render(request, 'seller_dashboard.html')


# Password Reset Views
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Generate reset code
            reset_code = f"{random.randint(100000, 999999)}"
            
            # Store reset data in session
            request.session['password_reset'] = {
                'email': email,
                'code': reset_code,
                'timestamp': time.time()
            }
            
            # Send email
            try:
                send_mail(
                    subject='Password Reset Code',
                    message=f'Your password reset code is: {reset_code}\n\nThis code will expire in 15 minutes.',
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[email],
                    fail_silently=not settings.DEBUG,
                )
                messages.success(request, f'Password reset code has been sent to {email}')
                return redirect('verify_reset_code')
            except Exception as e:
                messages.error(request, 'Failed to send email. Please try again.')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})


def verify_reset_code(request):
    reset_data = request.session.get('password_reset')
    if not reset_data:
        messages.error(request, 'No password reset request found. Please start again.')
        return redirect('forgot_password')
    
    # Check if code has expired (15 minutes)
    import time
    if time.time() - reset_data['timestamp'] > 900:  # 15 minutes = 900 seconds
        del request.session['password_reset']
        messages.error(request, 'Reset code has expired. Please request a new one.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = VerifyResetCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == reset_data['code']:
                # Mark code as verified
                reset_data['verified'] = True
                request.session['password_reset'] = reset_data
                return redirect('set_new_password')
            else:
                messages.error(request, 'Invalid reset code. Please try again.')
    else:
        form = VerifyResetCodeForm()
    
    return render(request, 'verify_reset_code.html', {
        'form': form, 
        'email': reset_data['email']
    })


def resend_reset_code(request):
    from django.http import JsonResponse
    import time
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    reset_data = request.session.get('password_reset')
    if not reset_data:
        return JsonResponse({'error': 'No password reset request found'}, status=400)
    
    # Check rate limiting (60 seconds)
    last_resend = request.session.get('last_reset_resend_time', 0)
    current_time = time.time()
    if current_time - last_resend < 60:
        remaining = 60 - (current_time - last_resend)
        return JsonResponse({'error': f'Please wait {int(remaining)} more seconds'}, status=429)
    
    # Generate new reset code
    new_code = f"{random.randint(100000, 999999)}"
    reset_data['code'] = new_code
    reset_data['timestamp'] = current_time
    request.session['password_reset'] = reset_data
    request.session['last_reset_resend_time'] = current_time
    
    # Send email
    try:
        send_mail(
            subject='New Password Reset Code',
            message=f'Your new password reset code is: {new_code}\n\nThis code will expire in 15 minutes.',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[reset_data['email']],
            fail_silently=not settings.DEBUG,
        )
        return JsonResponse({'success': True, 'message': 'New reset code sent successfully'})
    except Exception as e:
        return JsonResponse({'error': 'Failed to send email'}, status=500)


def set_new_password(request):
    reset_data = request.session.get('password_reset')
    if not reset_data or not reset_data.get('verified'):
        messages.error(request, 'Please verify your reset code first.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            # Get user and update password
            try:
                user = User.objects.get(email=reset_data['email'])
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Clear session
                try:
                    del request.session['password_reset']
                    if 'last_reset_resend_time' in request.session:
                        del request.session['last_reset_resend_time']
                except KeyError:
                    pass
                
                messages.success(request, 'Password has been successfully updated. You can now login with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User account not found.')
                return redirect('forgot_password')
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'set_new_password.html', {
        'form': form,
        'email': reset_data['email']
    })
