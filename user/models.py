from django.db import models
from django.conf import settings

# Model untuk Portofolio, Keuntungan, dan RDN Wallet
class UserPortfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")
    nilai_portofolio = models.BigIntegerField(default=0)  # Default Rp 0
    keuntungan = models.BigIntegerField(default=0)  # Default Rp 0
    rdn_wallet = models.BigIntegerField(default=0)  # Default Rp 0

    def __str__(self):
        return f"Portfolio for {self.user.email}"


# Relasi antara User dan Produk yang dibeli
class UserProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    produk = models.ForeignKey("backend.Produk", on_delete=models.CASCADE, related_name="pembelian")  # Perbaiki referensi
    jumlah_beli = models.PositiveIntegerField(default=1)
    total_harga = models.BigIntegerField()

    def save(self, *args, **kwargs):
        # Kalkulasi total harga berdasarkan harga saham dan jumlah beli
        self.total_harga = self.jumlah_beli * self.produk.harga_saham
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} membeli {self.produk.nama_saham} ({self.jumlah_beli} saham)"
    

class RDNWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rdn_wallet')
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class RDNTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]

    wallet = models.ForeignKey(RDNWallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_number = models.CharField(max_length=20, unique=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.BigIntegerField()
    method = models.CharField(max_length=50)
    fee = models.BigIntegerField(default=0)
    total = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.transaction_number}"
