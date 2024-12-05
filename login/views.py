from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from login.models import CustomUser 
from django.shortcuts import render, redirect
from login.forms import RegisterForm
from django.utils.timezone import now

def generate_rdn():
    # Format tanggal: DDMMYYYY
    date_part = datetime.now().strftime('%d%m%Y')
    # Angka acak 3 digit
    random_part = str(random.randint(100, 999))
    return f"{date_part}{random_part}"

@receiver(post_save, sender=CustomUser)
def create_rdn_for_user(sender, instance, created, **kwargs):
    if created and instance.is_staff is False:  # Hanya untuk user non-admin
        if not instance.rdn:  # Jika belum ada RDN
            instance.rdn = generate_rdn()
            instance.save()

def login_view(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Menggunakan authenticate untuk login dengan email
        user = authenticate(request, email=email, password=password)
        
        if user is not None:  # Jika user berhasil ditemukan
            login(request, user)  # Login user
            # Arahkan berdasarkan role
            if user.role == 'admin':
                return redirect('dashboard')  # URL untuk admin
            elif user.role == 'user':
                return redirect('user_dashboard')  # URL untuk user
        else:
            error_message = 'Email atau password salah.'
    
    return render(request, 'auth/login_page.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('')  # URL untuk landing page


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Set date_joined as the current time
            form.instance.date_joined = now()
            form.save()
            return redirect('login')  # Redirect ke halaman login setelah sukses register
    else:
        form = RegisterForm()

    return render(request, 'auth/register_page.html', {'form': form})

def forgot_password_view(request):
    return render(request, 'auth_app/forgot_password.html')
 