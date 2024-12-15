from django.shortcuts import render,HttpResponse
from turtle import title
from django.contrib.auth.decorators import login_required
from .models import KategoriArtikel, Article, MonthlyReport
from django.db import models
from .forms import ArticleForm
from django.contrib import messages
from login.models import CustomUser  
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produk
from .forms import ProdukForm
from django.utils import timezone
from user.models import StockTransaction
from django.utils.timezone import now
from django.db.models import Case, When, Value, CharField, Sum, Q
from django.db.models import F, Max
from django.db.models.functions import Concat
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Coalesce


@login_required
def dashboard(request):
    jumlah_artikel = Article.objects.count()
    jumlah_user = CustomUser.objects.filter(role='user').count()
    jumlah_saham = Produk.objects.filter(jenis_saham='konvensional').count()
    jumlah_sSyariah = Produk.objects.filter(jenis_saham='syariah').count()
    context={
        'title':title,
        'jumlah_artikel': jumlah_artikel,
        'jumlah_user': jumlah_user,
        'jumlah_saham': jumlah_saham,
        'jumlah_sSyariah': jumlah_sSyariah,
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
def edit_kategori(request, pk):
    kategori = get_object_or_404(KategoriArtikel, pk=pk) 
    if request.method == 'POST':
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        if nama:  
            kategori.nama = nama
            kategori.deskripsi = deskripsi
            kategori.save()
            messages.success(request, "Kategori berhasil diperbarui!")
            return redirect('list_kategori')
        else:
            messages.error(request, "Nama kategori tidak boleh kosong!")
    
    context = {
        'title': 'Edit Kategori',
        'kategori': kategori,
    }
    return render(request, 'pages/artikel/update_kategori.html', context)

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


@login_required
def data_user(request):
    data_user = CustomUser.objects.filter(role='user')
    context={
        'title':title,
        'data_user' : data_user
    }
    return render(request, 'pages/akun_user/a_user.html', context)

@login_required
def generate_monthly_report(user):
    current_month = timezone.now().replace(day=1)
    
    if MonthlyReport.objects.filter(user=user, report_month=current_month).exists():
        return f"Laporan untuk {user.username} sudah dibuat."

    syariah_amount = StockTransaction.objects.filter(
        user=user, 
        stock_type='syariah', 
        transaction_date__month=current_month.month,
        transaction_date__year=current_month.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    konvensional_amount = StockTransaction.objects.filter(
        user=user, 
        stock_type='konvensional', 
        transaction_date__month=current_month.month,
        transaction_date__year=current_month.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    report = MonthlyReport.objects.create(
        user=user,
        report_month=current_month,
        status='Belum Dicek',
    )
    return f"Laporan berhasil dibuat untuk {user.username}."



@login_required
def monthly_report_list(request):
    from datetime import datetime
    current_month = datetime.now().replace(day=1)  # Bulan berjalan (tanggal 1)

    data_list = CustomUser.objects.annotate(
        syariah_total=Sum('stock_transactions__amount', filter=Q(stock_transactions__stock_type='syariah')),
        konvensional_total=Sum('stock_transactions__amount', filter=Q(stock_transactions__stock_type='konvensional')),
        jenis_investasi=Concat(
            Case(
                When(syariah_total__gt=0, then=Value("Saham Syariah")),
                default=Value(""),
                output_field=CharField()
            ),
            Case(
                When(konvensional_total__gt=0, then=Value(", Saham Konvensional")),
                default=Value(""),
                output_field=CharField()
            ),
            output_field=CharField()
        ),
        laporan_bulanan=Coalesce(   
            Subquery(
                MonthlyReport.objects.filter(
                    user=OuterRef('id'), 
                    report_month=current_month
                ).values('status')[:1]
            ),
            Value("Belum Ada Laporan"),   
            output_field=CharField()
        )
    ).filter(Q(syariah_total__gt=0) | Q(konvensional_total__gt=0))   

    context = {
        'data_list': data_list
    }
    return render(request, 'pages/laporan_admin/laporan_admin.html', context)



def reset_monthly_report_status():
    current_month = now().replace(day=1)
    MonthlyReport.objects.filter(report_month__lt=current_month).update(status='Belum Dicek')