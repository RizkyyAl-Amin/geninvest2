from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
 



class KategoriArtikel(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class Article(models.Model):
    judul = models.CharField(max_length=255)
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey ke User
    kategori = models.ForeignKey('KategoriArtikel', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='artikel_cover/', null=True, blank=True)
    konten = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.judul

class Produk(models.Model):
    kode_saham = models.CharField(max_length=10, unique=True)
    nama_perusahaan = models.CharField(max_length=100)
    jenis_saham = models.CharField(max_length=20)
    saham = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nama_saham    


class DataUser(models.Model):
    kode_saham = models.CharField(max_length=10, unique=True)
    nama_perusahaan = models.CharField(max_length=100)
    jenis_saham = models.CharField(max_length=20)
    saham = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nama_saham    


class MonthlyReport(models.Model):
    STATUS_CHOICES = [
        ('Belum Dicek', 'Belum Dicek'),
        ('Ceklist', 'Ceklist'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='monthly_reports'
    )
    report_month = models.DateField(default=now)
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='Belum Dicek'
    )
    report_file = models.FileField(
        upload_to='reports/', 
        null=True, 
        blank=True, 
        validators=[FileExtensionValidator(['pdf'])],
        help_text="Upload PDF laporan bulanan"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        month_year = self.report_month.strftime('%B %Y')
        return f"Laporan {self.user.username} - {month_year} - {self.status}"