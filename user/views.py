from django.shortcuts import render,HttpResponse
from turtle import title
from django.contrib.auth.decorators import login_required
from backend.models import Produk, Article
from django.db import models
from django.shortcuts import render, redirect

from django.contrib import messages
from login.models import CustomUser  
from django.shortcuts import render, redirect, get_object_or_404
 
from django.contrib.auth.decorators import login_required

@login_required
def u_dashboard(request):
    jumlah_artikel = Article.objects.count()
    jumlah_user = CustomUser.objects.all()
    produks_list = Produk.objects.all()
    context={
        'title':title,
        'jumlah_artikel': jumlah_artikel,
        'jumlah_user': jumlah_user,
        'produk_list' : produks_list
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def wallet(request):
    jumlah_user = CustomUser.objects.all()
    context={
        'title':title,
        'jumlah_user': jumlah_user
    }
    return render(request, 'pages/wallet.html', context)


def porto(request):
    
    context={
        'title':title,
         
    }
    return render(request, 'pages/porto.html', context)


def jual(request):
    
    context={
        'title':title,
         
    }
    return render(request, 'pages/jual.html', context)

def beli(request):
    
    context={
        'title':title,
         
    }
    return render(request, 'pages/beli.html', context)