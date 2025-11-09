from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import django.contrib.auth as auth
import django.contrib.messages as messages

from user.forms import EditFullNameForm, EditPasswordForm

# Create your views here.
def dashboard(request):
    data = {}
    return render(request, 'pages/dashboard.html', data)

def settings(request):
    fullname_form = EditFullNameForm(initial={'fullname': request.user.get_full_name()})
    password_form = EditPasswordForm(user=request.user)

    context = {
        'fullname_form': fullname_form,
        'password_form': password_form,
    }
    return render(request, 'pages/settings.html', context)

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

    return redirect('settings')

def page_not_found(request, exception=None):
    data = {
        'exception': exception
    }
    return render(request, 'error/404.html', data)

def internal_server_error(request, exception=None):
    data = {
        'exception': exception
    }
    return render(request, 'error/500.html', data)