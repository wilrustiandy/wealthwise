from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
import django.contrib.auth as auth
import django.contrib.messages as messages

from user.forms import UserForm

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
                    messages.error(request, "Registration failed!")
                    print("Form errors:", form.errors)

            except IntegrityError as e:
                messages.error(request, "Registration failed!")
                return redirect('internal-server-error', e)

    data = {
        'form': form
    }
    return render(request, 'pages/user/register.html', data)