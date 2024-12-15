from django.db import models
from django.conf import settings
from login.models import RDNWalletDetail  
from django.utils import timezone
import random


class UserPortfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")
    nilai_portofolio = models.BigIntegerField(default=0)  
    keuntungan = models.BigIntegerField(default=0)  
    rdn_wallet = models.BigIntegerField(default=0)  

    def __str__(self):
        return f"Portfolio for {self.user.email}"


class UserProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    produk = models.ForeignKey("backend.Produk", on_delete=models.CASCADE, related_name="pembelian") 
    jumlah_beli = models.PositiveIntegerField(default=1)
    total_harga = models.BigIntegerField()

    def save(self, *args, **kwargs):
        self.total_harga = self.jumlah_beli * self.produk.harga_saham
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} membeli {self.produk.nama_saham} ({self.jumlah_beli} saham)"
    

 

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
    
class StockTransaction(models.Model):
    STOCK_TYPES = [
        ('konvensional', 'Saham Konvensional'),
        ('syariah', 'Saham Syariah'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stock_transactions'   
    )
    stock_type = models.CharField(max_length=15, choices=STOCK_TYPES)
    amount = models.BigIntegerField()
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            date_str = timezone.now().strftime('%Y%m%d')  # Format tanggal YYYYMMDD
            random_digits = f"{random.randint(10000, 99999)}"  # Lima angka acak
            self.transaction_number = f"{date_str}{random_digits}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.stock_type} - {self.amount} - {self.transaction_number}"
    
