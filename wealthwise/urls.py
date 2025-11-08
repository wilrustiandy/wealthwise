"""
URL configuration for wealthwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib.auth.decorators import login_required

from core import views as core_views
from user import views as user_views

urlpatterns = [
    # Dashboard
    url(r'^$', login_required(core_views.dashboard), name="dashboard"),
    url(r'^dashboard$', login_required(core_views.dashboard), name="dashboard"),

    # User
    url(r'^user/login$', user_views.login, name="user-login"),
    url(r'^user/logout$', user_views.logout, name="user-logout"),
    url(r'^user/register$', user_views.register, name="user-register"),

    # Error
    url(r'error', core_views.internal_server_error, name="internal-server-error"),
    url(r'.*', core_views.page_not_found, name="page-not-found"),
]