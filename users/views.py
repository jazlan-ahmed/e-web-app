from django.shortcuts import render, redirect
from .form import UserRegisterForm, UserLoginForm, UserAddress
from .models import Address
from django.contrib.auth import authenticate, login, logout

    
def user_registeration(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login')
    return render(request, 'register.html', {'form':form})

def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user:
                login(request, user)
                return redirect('index')
    return render(request, 'login.html', {'form':form})