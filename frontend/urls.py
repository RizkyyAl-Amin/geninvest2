from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('artikel',views.artikel,name='artikel'),
    path('artikel1',views.artikel1,name='artikel1'),
    path('kebijakan_privasi',views.kebijakan_privasi,name='kebijakan_privasi'),
    path('investasi',views.investasi,name='investasi'),
    path('pusat_bantuan/faq',views.faq,name='pusat_bantuan/faq'),
]