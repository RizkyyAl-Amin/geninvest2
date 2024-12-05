from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
    nama_saham = models.CharField(max_length=50)
    nama_perusahaan = models.CharField(max_length=100)
    jenis_saham = models.CharField(max_length=20)
    harga_saham = models.BigIntegerField()
    dividen_saham = models.IntegerField()
    minimal_beli = models.BigIntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField()
    def __str__(self):
        return self.nama_saham    


