from django.shortcuts import render,HttpResponse
from turtle import title
from django.contrib.auth.decorators import login_required
from .models import KategoriArtikel, Article
from django.db import models
from django.shortcuts import render, redirect
from .forms import ArticleForm
from django.contrib import messages
from login.models import CustomUser  
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from .forms import ProdukForm

@login_required
def dashboard(request):
    jumlah_artikel = Article.objects.count()
    jumlah_user = CustomUser.objects.filter(role='user').count()
    context={
        'title':title,
        'jumlah_artikel': jumlah_artikel,
        'jumlah_user': jumlah_user,
    }
    return render(request, 'dashboard.html', context)

@login_required
def art(request):
    articles = Article.objects.all()
    context = {
        'title': 'Data Artikel',
        'articles': articles
    }
    return render(request, 'pages/artikel/artikel2.html', context)


@login_required
def cartikel(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            artikel = form.save(commit=False)  # Jangan langsung simpan ke database
            artikel.penulis = request.user    # Isi field penulis dengan user login
            artikel.save()                    # Simpan setelah field diisi
            messages.success(request, "Artikel berhasil ditambahkan!")
            return redirect('art')  
        else:
            # Tambahkan pesan error untuk debugging
            messages.error(request, "Form tidak valid. Silakan periksa input Anda.")
            print(form.errors)  # Debugging di terminal
    else:
        form = ArticleForm()
    
    kategoris = KategoriArtikel.objects.all()
    context = {
        'title': 'Tambah Artikel',
        'form': form,
        'kategoris': kategoris,
    }
    return render(request, 'pages/artikel/create_artikel.html', context)

@login_required
def edit_artikel(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Artikel berhasil diperbarui!")
            return redirect('art')
    else:
        form = ArticleForm(instance=article)
    kategoris = KategoriArtikel.objects.all()
    context = {
        'title': 'Edit Artikel',
        'form': form,
        'article': article,
        'kategoris': kategoris,
    }
    return render(request, 'pages/artikel/update_artikel.html', context)


@login_required
def delete_artikel(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Artikel berhasil dihapus!")
        return redirect('art')

    context = {
        'title': 'Hapus Artikel',
        'article': article
    }
    return render(request, 'pages/artikel/delete_artikel.html', context)

@login_required
def list_kategori(request):
    kategoris = KategoriArtikel.objects.all()
    context = {
        'title': 'Data Kategori Artikel',
        'kategoris': kategoris,
    }
    return render(request, 'pages/artikel/kategori_artikel.html', context)

@login_required
def create_kategori(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        KategoriArtikel.objects.create(nama=nama, deskripsi=deskripsi)
        messages.success(request, "Kategori berhasil ditambahkan!")
        return redirect('list_kategori')
    return render(request, 'pages/artikel/create_kategori.html', {'title': 'Tambah Kategori'})

@login_required
def delete_kategori(request, pk):
    kategori = get_object_or_404(KategoriArtikel, pk=pk)
    if request.method == 'POST':
        kategori.delete()
        messages.success(request, "Kategori berhasil dihapus!")
        return redirect('list_kategori')
    return render(request, 'pages/artikel/delete_kategori.html', {'title': 'Hapus Kategori', 'kategori': kategori})

@login_required
def list_produk(request):
    produks = Produk.objects.all()
    return render(request, 'pages/produk/produk.html', {'produks': produks})

@login_required
def create_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('list_produk')
    else:
        form = ProdukForm()
    return render(request, 'pages/produk/create_produk.html', {'form': form})

@login_required
def update_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui!')
            return redirect('list_produk')
    else:
        form = ProdukForm(instance=produk)
    return render(request, 'pages/produk/update.html', {'form': form, 'produk': produk})

@login_required
def delete_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        messages.success(request, 'Produk berhasil dihapus!')
        return redirect('list_produk')
    return render(request, 'pages/produk/delete.html', {'produk': produk})
