from django.shortcuts import render,HttpResponse
from turtle import title
from backend.models import Produk
from django.core.paginator import Paginator
from backend.models import Article


# Create your views here.
def home(request):
    articles = Article.objects.all()
    context={
        'title':title,
        'articles': articles
    }
    return render(request, 'home.html', context)

def artikel(request):
    articles = Article.objects.all()
    context={
        'title':title,
        'articles': articles
    }
    return render(request, 'pages/artikel/artikel.html', context)

def artikel1(request):
    context={
        'title':title
    }
    return render(request, 'pages/artikel/artikel1.html', context)


def kebijakan_privasi(request):
    context={
        'title':title
    }
    return render(request, 'pages/kebijakan_privasi.html', context)

def investasi(request):
    produks_list = Produk.objects.all()
    paginator = Paginator(produks_list, 10)
    page_number = request.GET.get('page')
    produks = paginator.get_page(page_number)
    context={
        'title':title,
        'produks' : produks
    }
    return render(request, 'pages/investasi.html', context)

def faq(request):
    context={
        'title':title
    }
    return render(request, 'pages/pusat_bantuan/faq.html', context)
