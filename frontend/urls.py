from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('artikel',views.artikel,name='artikel'),
    path('artikel1',views.artikel1,name='artikel1'),
    path('pusat_bantuan/faq',views.faq,name='pusat_bantuan/faq'),
    path('pusat_bantuan/syarat_ketentuan',views.syarat_ket,name='pusat_bantuan/syarat_ketentuan'),
]