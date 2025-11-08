from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
import django.contrib.auth as auth
import django.contrib.messages as messages

from user.forms import UserForm

# Create your views here.
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
                    return redirect('dashboard')
                
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