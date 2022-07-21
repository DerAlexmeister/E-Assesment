import urllib.parse
import json

from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/learninganalytics/')
        else:
            return redirect('/eassessments/')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username = username, password = password)
        if user is not None:
            if(user.is_superuser):
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.info(request, "invalid credentials")
            return redirect("admin")
         
    return render(request,'login.html') 

def user_logout(request):
    print('Loggin out {}'.format(request.user))
    auth.logout(request)
    print(request.user)
    return render(request,'logout.html') 