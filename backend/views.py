from django.shortcuts import render,HttpResponse
from turtle import title

# Create your views here.
def dashboard(request):
    context={
        'title':title
    }
    return render(request, 'dashboard.html', context)

def login(request):
    context={
        'title':title
    }
    return render(request, 'pages/auth/login_page.html', context)

def art(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/artikel2.html', context)

def kategori(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/kategori_artikel.html', context)


def produk(request):
    context={
        'title':title
    }
    return render(request, 'pages/produk/produk.html', context)

def cproduk(request):
    context={
        'title':title
    }
    return render(request, 'pages/produk/create_produk.html', context)

def cartikel(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/create_artikel.html', context)
