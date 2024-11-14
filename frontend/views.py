from django.shortcuts import render,HttpResponse
from turtle import title

# Create your views here.
def home(request):
    context={
        'title':title
    }
    return render(request, 'home.html', context)

def artikel(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/artikel.html', context)

def artikel1(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/artikel1.html', context)

def faq(request):
    context={
        'title':title
    }
    return render(request, 'pages/pusat_bantuan/faq.html', context)

def syarat_ket(request):
    context={
        'title':title
    }
    return render(request, 'pages/pusat_bantuan/syarat_ket.html', context)
