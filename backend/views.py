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
from django.utils.timezone import now
from django.db.models import Case, When, Value, CharField, Sum, Q, Func
from django.db.models import F, Max
from django.db.models.functions import Concat
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import render
from user.models import Transaction, StockTransaction
from itertools import chain
from .forms import MonthlyReportForm
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MonthlyReport  # Ganti dengan nama model yang sesuai

from django.http import JsonResponse
from django.core.paginator import Paginator
from itertools import chain
from django.http import JsonResponse


from django.db.models.functions import Concat, Coalesce
from django.db.models import Case, When, Value, CharField, Sum, Q, Subquery, OuterRef

from django.db.models import Case, When, Value, CharField, F
from django.db.models.functions import Concat
from itertools import chain
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    jumlah_artikel = Article.objects.count()
    jumlah_user = CustomUser.objects.filter(role='user').count()
    jumlah_saham = Produk.objects.filter(jenis_saham='konvensional').count()
    jumlah_sSyariah = Produk.objects.filter(jenis_saham='syariah').count()
    jumlah_pembelian = StockTransaction.objects.count()
    jumlah_penarikan = Transaction.objects.filter(transaction_type='withdraw').count()
    context={
        'title':title,
        'jumlah_artikel': jumlah_artikel,
        'jumlah_user': jumlah_user,
        'jumlah_saham': jumlah_saham,
        'jumlah_sSyariah': jumlah_sSyariah,
        'jumlah_pembelian' : jumlah_pembelian,
        'jumlah_penarikan' : jumlah_penarikan
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
    
    data_user = CustomUser.objects.filter(role='user').annotate(
    
        balance=F('wallet__balance') 
    )
    
    context = {
        'title': "Data User",
        'data_user': data_user,
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


def update_monthly_report(request, id):
    # Ambil data laporan bulanan
    report = get_object_or_404(MonthlyReport, user_id=id)
    user = report.user

    # Ambil semua transaksi saham terkait user
    transactions = user.stock_transactions.all()

    # Hitung total berdasarkan jenis saham
    syariah_total = transactions.filter(stock_type='syariah').aggregate(total=Sum('amount'))['total'] or 0
    konvensional_total = transactions.filter(stock_type='konvensional').aggregate(total=Sum('amount'))['total'] or 0

    # Tentukan jenis investasi
    if syariah_total > 0 and konvensional_total > 0:
        jenis_investasi = "Saham Syariah, Saham Konvensional"
    elif syariah_total > 0:
        jenis_investasi = "Saham Syariah"
    elif konvensional_total > 0:
        jenis_investasi = "Saham Konvensional"
    else:
        jenis_investasi = "Tidak Ada"

    if request.method == "POST":
        form = MonthlyReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            # Simpan data laporan
            updated_report = form.save(commit=False)

            # Ubah status menjadi 'Ceklist'
            updated_report.status = 'Ceklist'

            # Hitung total keseluruhan
            updated_report.total = syariah_total + konvensional_total + updated_report.imba_hasil

            # Simpan perubahan
            updated_report.save()

            messages.success(request, "Laporan bulanan berhasil diperbarui.")
            return redirect('monthly_report_list')
        else:
            messages.error(request, "Terjadi kesalahan. Mohon cek kembali data Anda.")
    else:
        form = MonthlyReportForm(instance=report)

    # Data untuk template
    context = {
        "data": {
            "id": report.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "jenis_investasi": jenis_investasi,
            "syariah_total": syariah_total,
            "konvensional_total": konvensional_total,
            "total_investasi": syariah_total + konvensional_total,
            "imba_hasil": report.imba_hasil,
            "total": report.total,
        },
        "form": form,
    }
    return render(request, "pages/laporan_admin/update_laporan_admin.html", context)




@login_required
def monthly_report_list(request):
    from datetime import datetime
    from django.db.models import F, Sum, Value, CharField, Subquery, OuterRef, Case, When
    from django.db.models.functions import Coalesce, Concat

    current_month = datetime.now().replace(day=1)  # Bulan berjalan (tanggal 1)
    id=F('id') 
    data_list = CustomUser.objects.annotate(
        syariah_total=Coalesce(
            Sum('stock_transactions__amount', filter=Q(stock_transactions__stock_type='syariah')), 
            Value(0)
        ),
        konvensional_total=Coalesce(
            Sum('stock_transactions__amount', filter=Q(stock_transactions__stock_type='konvensional')), 
            Value(0)
        ),
        total_investasi=F('syariah_total') + F('konvensional_total'),
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
        laporan_bulanan_status=Coalesce(   
            Subquery(
                MonthlyReport.objects.filter(
                    user=OuterRef('id'), 
                    report_month=current_month
                ).values('status')[:1]
            ),
            Value("Belum Ada Laporan"),   
            output_field=CharField()
        ),
        laporan_bulanan_file=Subquery(
        MonthlyReport.objects.filter(
            user=OuterRef('id'), 
            report_month=current_month
        ).values('report_file')[:1]
            ),
        
        imba_hasil=Coalesce(
            Subquery(
                MonthlyReport.objects.filter(
                    user=OuterRef('id'), 
                    report_month=current_month
                ).values('imba_hasil')[:1]
            ),
            Value(0)
        ),
        total_imba_hasil=Coalesce(
            Sum('monthly_reports__imba_hasil'), 
            Value(0)
        ),
        total_keseluruhan=F('total_investasi') + F('total_imba_hasil'),
    ).filter(
        Q(syariah_total__gt=0) | Q(konvensional_total__gt=0)
    )   

    context = {
        'data_list': data_list
    }
    return render(request, 'pages/laporan_admin/laporan_admin.html', context)

def reset_monthly_report_status():
    current_month = now().replace(day=1)
    MonthlyReport.objects.filter(report_month__lt=current_month).update(status='Belum Dicek')




@login_required
def riwayat_transaksi(request):
    # Ambil semua data transaksi dari tabel Transaction
    transactions = Transaction.objects.all().annotate(
        date=F('created_at'),
        transaction_amount=F('amount'),  # Alias untuk jumlah transaksi
        activity=Case(
            When(transaction_type__isnull=False, then=Concat(Value(''), F('transaction_type'))),
            default=Value('Tidak Diketahui'),
            output_field=CharField()
        ),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        rdn=F('user__rdn'),  # Ambil nomor RDN dari relasi ke User
        source=Value('Transaction', output_field=CharField())  # Menandai sumber data
    )

    # Ambil semua data transaksi dari tabel StockTransaction
    stock_transactions = StockTransaction.objects.all().annotate(
        date=F('transaction_date'),
        transaction_amount=F('amount'),  # Alias untuk jumlah transaksi
        activity=Case(
            When(stock_type__isnull=False, then=Concat(Value('Saham '), F('stock_type'))),  # Tambahkan "Saham" di depan
            default=Value('Tidak Diketahui'),
            output_field=CharField()
        ),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        rdn=F('user__rdn'),  # Ambil nomor RDN dari relasi ke User
        source=Value('StockTransaction', output_field=CharField())  # Menandai sumber data
    )

    # Gabungkan kedua queryset
    combined_transactions = chain(transactions, stock_transactions)

    # Kirimkan data ke template
    return render(request, 'pages/riwayat_admin/riwayat_transaksia.html', {'transactions': combined_transactions})


@login_required
def transaksi_data(request):
    from django.utils.formats import number_format  # Built-in Django number formatter

    # Ambil semua data transaksi
    transactions = Transaction.objects.all().annotate(
        date=F('created_at'),
        transaction_amount=F('amount'),
        activity=Case(
            When(transaction_type__isnull=False, then=Concat(Value(''), F('transaction_type'))),
            default=Value('Tidak Diketahui'),
            output_field=CharField()
        ),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        rdn=F('user__rdn'),
        source=Value('Transaction', output_field=CharField())
    ).values('date', 'transaction_amount', 'activity', 'first_name', 'last_name', 'rdn', 'source')

    # Format transaction_amount
    for transaction in transactions:
        transaction['transaction_amount'] = f"Rp {number_format(transaction['transaction_amount'], decimal_pos=0, use_l10n=True)}"

    return JsonResponse({'data': list(transactions)})
