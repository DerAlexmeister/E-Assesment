"""EAssLAna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.shortcuts import redirect

from .views import user_login
from .views import user_logout

urlpatterns = [
    path("", lambda request: redirect('accounts/login/', permanent=True)),
    path('admin/', admin.site.urls),
    path("accounts/logout/", user_logout),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", user_login),
    
    path('eassessments/', include('EAss.urls')),
    path('learninganalytics/', include('LAna.urls')),
]

