from django.shortcuts import render,HttpResponse
from turtle import title
from django.contrib.auth.decorators import login_required
from backend.models import Produk, Article, MonthlyReport
from django.db import models
from login.models import RDNWalletDetail
from django.contrib import messages
from login.models import CustomUser  
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings
from .models import StockTransaction
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.utils.timezone import now
import datetime

@login_required
def u_dashboard(request):
    from django.db.models import Sum

    jumlah_artikel = Article.objects.count()
    jumlah_user = CustomUser.objects.all()
    produks_list = Produk.objects.all()
    rdn_data = RDNWalletDetail.objects.filter(user=request.user).first()
    
   
    pembelian_syariah = StockTransaction.objects.filter(
        user=request.user, stock_type="Syariah"
    ).values("transaction_date").annotate(total=Sum("amount"))
    pembelian_konvensional = StockTransaction.objects.filter(
        user=request.user, stock_type="Konvensional"
    ).values("transaction_date").annotate(total=Sum("amount"))

    context = {
        'title': title,
        'jumlah_artikel': jumlah_artikel,
        'jumlah_user': jumlah_user,
        'produk_list': produks_list,
        'rdn_data': rdn_data,
        'pembelian_syariah': list(pembelian_syariah),
        'pembelian_konvensional': list(pembelian_konvensional),
    }
    return render(request, 'user_dashboard.html', context)

 

@login_required
def wallet(request):
    jumlah_user = CustomUser.objects.all()
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(transactions, 10)  # 10 transaksi per halaman
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    try:
        rdn_data = RDNWalletDetail.objects.get(user=request.user)
    except RDNWalletDetail.DoesNotExist:
        rdn_data = None
    context={
        'title':title,
        'jumlah_user': jumlah_user,
        'rdn_data' : rdn_data,
        'transactions': transactions
        
    }
    return render(request, 'pages/wallet.html', context)


def porto(request):
    
    context={
        'title':title,
         
    }
    return render(request, 'pages/porto.html', context)


def jual(request):
    produks_list = Produk.objects.all()
    context={
        'title':title,
         'produk_list' : produks_list
    }
    return render(request, 'pages/jual.html', context)

def beli(request):
    produks_list = Produk.objects.all()
    context={
        'title':title,
         'produk_list' : produks_list
    }
    return render(request, 'pages/beli.html', context)


@csrf_exempt
@login_required
def deposit(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            wallet = get_object_or_404(RDNWalletDetail, user=request.user)
            wallet.balance += amount
            wallet.save()
            
            # Simpan transaksi
            Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                amount=amount
            )
            return JsonResponse({'success': True, 'new_balance': wallet.balance})
        return JsonResponse({'success': False, 'error': 'Invalid deposit amount'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        wallet = get_object_or_404(RDNWalletDetail, user=request.user)
        fee = 2500  # Biaya withdraw tetap
        total_withdraw = amount + fee
        if amount > 0 and wallet.balance >= total_withdraw:
            wallet.balance -= total_withdraw
            wallet.save()
            
            # Simpan transaksi
            Transaction.objects.create(
                user=request.user,
                transaction_type='withdraw',
                amount=amount
            )
            return JsonResponse({'success': True, 'new_balance': wallet.balance})
        return JsonResponse({'success': False, 'error': 'Saldo tidak mencukupi atau jumlah tidak valid'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

 
@login_required
@csrf_exempt
def buy_stock(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stock_type = data.get('stock_type')
            amount = int(data.get('amount'))

            if not stock_type or not amount:
                return JsonResponse({'success': False, 'message': 'Data tidak lengkap.'})
 
            wallet = RDNWalletDetail.objects.get(user=request.user)

           
            if wallet.balance < amount:
                return JsonResponse({'success': False, 'message': 'Saldo tidak mencukupi.'})

           
            wallet.balance -= amount
            wallet.save()

          
            StockTransaction.objects.create(
                user=request.user,
                stock_type=stock_type,
                amount=amount,
                transaction_date=timezone.now()
            )
            
     
            from datetime import datetime

    
            current_month = datetime.now().replace(day=1)  
            report_exists = MonthlyReport.objects.filter(
                user=request.user, 
                report_month=current_month
            ).exists()

            if not report_exists:
           
                MonthlyReport.objects.create(
                    user=request.user,
                    report_month=current_month,
                    status='Belum Dicek'  
                )

            print("Transaksi berhasil disimpan dan laporan bulanan diperbarui.")
            return JsonResponse({
                'success': True,
                'message': 'Pembelian saham berhasil.',
                'new_balance': wallet.balance
            })

        except RDNWalletDetail.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet tidak ditemukan.'})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
