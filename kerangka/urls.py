from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('artikel',views.artikel,name='artikel'),
    path('artikel1',views.artikel1,name='artikel1'),
    path('pusat_bantuan',views.pusat_bantuan,name='pusat_bantuan'),
]