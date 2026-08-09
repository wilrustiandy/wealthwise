from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.utils.safestring import mark_safe
import django.contrib.auth as auth
import django.contrib.messages as messages

from user.forms import UserForm, EditProfileForm, EditFullNameForm, EditPasswordForm
from core.utils import get_form_errors

# Create your views here.
def login(request):
    if request.method == "POST":
        username_or_email = request.POST['usernameOrEmail']
        password = request.POST['password']
        
        # Try to get user by email
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email  # Assume they entered username

        # Authenticate using username
        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Login failed! Wrong username or password")

    return render(request, 'pages/user/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user-login')

def register(request):
    form = UserForm()

    if request.method == "POST":
        with transaction.atomic():
            try:
                form = UserForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['fullname']
                    )

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
    form = EditProfileForm(request.POST or None, instance=request.user)

    if request.method == "POST":
        with transaction.atomic():
            try:
                if form.is_valid():
                    form.save()
                    messages.success(request, "Profile updated successfully!")
                
                else:
                    error = get_form_errors(form.errors)
                    print("Form error: " + error)
                    messages.error(request, mark_safe(f"Update profile failed!!<br>{error}"))
            
            except IntegrityError as error:
                print("Integrity error: ", error)
                messages.error(request, mark_safe(f"Update profile failed!!<br>{str(error)}"))
                return redirect('internal-server-error', error)
    
    data = {
        'form': form
    }
    return render(request, 'pages/user/profile.html', data)

def edit_fullname(request):
    if request.method == "POST":
        form = EditFullNameForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            request.user.first_name = fullname  # or split into first_name/last_name if needed
            request.user.save()
            messages.success(request, "Full name updated successfully!")
        else:
            errors = "<br>".join([str(err) for err in form.errors.values()])
            messages.error(request, mark_safe(f"Failed to update full name<br>{errors}"))

    return redirect('settings')

def edit_password(request):
    if request.method == "POST":
        form = EditPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            auth.update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password changed successfully!")
        else:
            errors = "<br>".join([str(err) for err in form.errors.values()])
            messages.error(request, mark_safe(f"Failed to change password<br>{errors}"))

    return redirect('user-profile')