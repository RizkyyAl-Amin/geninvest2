from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard')  # URL untuk admin
            elif user.role == 'user':
                return redirect('user_dashboard')  # URL untuk user
        else:
            error_message = 'Username atau password salah.'
    
    return render(request, 'auth/login_page.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('')  # URL untuk landing page


def register_view(request):
    return render(request, 'auth_app/register.html')

def forgot_password_view(request):
    return render(request, 'auth_app/forgot_password.html')
