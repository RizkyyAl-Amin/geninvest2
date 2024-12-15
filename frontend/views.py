from django.shortcuts import render,HttpResponse
from turtle import title
from backend.models import Produk
from django.core.paginator import Paginator
from backend.models import Article
from backend.models import KategoriArtikel
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

# Create your views here.
def home(request):
    articles = Article.objects.order_by('-updated_at')[:3]

    context = {
        'title': 'Home',
        'articles': articles,   
    }
    return render(request, 'home.html', context)



def artikel(request):
    articles = Article.objects.all()
    categories = KategoriArtikel.objects.annotate(article_count=Count('article'))
    context = {
        'title': title,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'pages/artikel/artikel.html', context)

def artikel1(request, id):
    artikel = get_object_or_404(Article, id=id) 
    articles = Article.objects.exclude(id=id).order_by('-updated_at')[:5]
    articler = Article.objects.all().order_by('-updated_at')[:3]  
    categories = KategoriArtikel.objects.annotate(article_count=Count('article'))
    context = {
        'title': title,
        'artikel': artikel,
        'articles': articles,
        'articler': articler,
        'categories': categories,
    }
    return render(request, 'pages/artikel/artikel1.html', context)



def kebijakan_privasi(request):
    context={
        'title':title
    }
    return render(request, 'pages/pusat_bantuan.html', context)

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

