from django.shortcuts import render

# Create your views here.

# ========== Core ==========
def dashboard(request):
    data = {}
    return render(request, 'pages/dashboard.html', data)

# ========== Errors ==========
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