import urllib.parse
import json

from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from .forms import SignUpForm





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
    return render(request,'logout.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homeview')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})