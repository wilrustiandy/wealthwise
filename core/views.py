from django.shortcuts import render

# Create your views here.
def dashboard(request):
    data = {}
    return render(request, 'dashboard.html', data)