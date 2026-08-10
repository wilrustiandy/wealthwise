from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.utils.safestring import mark_safe

import django.contrib.auth as auth
import django.contrib.messages as messages

from user.forms import UserLoginForm, UserRegistrationForm, EditProfileForm, EditPasswordForm
from core.utils import get_form_errors

# Create your views here.
def login(request):
    form = UserLoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            print(form.cleaned_data)
            username_or_email = form.cleaned_data.get('username_email')
            password = form.cleaned_data.get('password')
            
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            
            except User.DoesNotExist:
                username = username_or_email

            user = auth.authenticate(request, username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            
            else:
                messages.error(request, "Login failed! Wrong username or password")
        
        else:
            error = get_form_errors(form.errors)
            print("Form error: " + error)
            messages.error(request, mark_safe(f"Login failed!!<br>{error}"))
    
    data = {
        'form': form
    }
    return render(request, 'pages/user/login.html', data)

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user-login')

def register(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == "POST":
        with transaction.atomic():
            try:
                if form.is_valid():
                    user = form.save()

                    auth.login(request, user)
                    messages.success(request, "Registration successful!")
                    return redirect('user-login')
                
                else:
                    error = get_form_errors(form.errors)
                    print("Form error: " + error)
                    messages.error(request, mark_safe(f"Registration failed!!<br>{error}"))

            except IntegrityError as error:
                print("Integrity error: ", error)
                messages.error(request, mark_safe(f"Registration failed!!<br>{str(error)}"))
                return redirect('internal-server-error', error)

    data = {
        'form': form
    }
    return render(request, 'pages/user/register.html', data)

def profile(request):
    profile_form = EditProfileForm(instance=request.user)
    password_form = EditPasswordForm(user=request.user)

    if request.method == "POST":
        if 'update_profile' in request.POST:
            with transaction.atomic():
                try:
                    profile_form = EditProfileForm(request.POST, instance=request.user)
                    if profile_form.is_valid():
                        profile_form.save()
                        messages.success(request, "Profile updated successfully!")
                        # return redirect('user-profile')
                    
                    else:
                        error = get_form_errors(profile_form.errors)
                        print("Form error: " + error)
                        messages.error(request, mark_safe(f"Update profile failed!!<br>{error}"))
                
                except IntegrityError as error:
                    print("Integrity error: ", error)
                    messages.error(request, mark_safe(f"Update profile failed!!<br>{str(error)}"))
                    return redirect('internal-server-error', error)
        
        elif 'edit_password' in request.POST:
            with transaction.atomic():
                try:
                    password_form = EditPasswordForm(request.POST, user=request.user)
                    if password_form.is_valid():
                        password_form.save(request=request)
                        messages.success(request, "Password changed successfully!")
                        # return redirect('user-profile')
                    
                    else:
                        errors = "<br>".join([str(err) for err in password_form.errors.values()])
                        messages.error(request, mark_safe(f"Failed to change password<br>{errors}"))
                
                except IntegrityError as error:
                    print("Integrity error: ", error)
                    messages.error(request, mark_safe(f"Change password failed!!<br>{str(error)}"))
                    return redirect('internal-server-error', error)
    
    data = {
        'profile_form': profile_form,
        'password_form': password_form
    }
    return render(request, 'pages/user/profile.html', data)