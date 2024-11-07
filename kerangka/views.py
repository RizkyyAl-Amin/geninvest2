from django.shortcuts import render,HttpResponse
from turtle import title

# Create your views here.
def home(request):
    context={
        'title':title
    }
    return render(request, 'frontend/home.html', context)

def artikel(request):
    context={
        'title':title
    }
    return render(request, 'frontend/pages/artikel.html', context)

def artikel1(request):
    context={
        'title':title
    }
    return render(request, 'frontend/pages/artikel1.html', context)

def pusat_bantuan(request):
    context={
        'title':title
    }
    return render(request, 'frontend/pages/pusat_bantuan.html', context)
