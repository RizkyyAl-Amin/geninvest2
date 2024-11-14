from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('art',views.art,name='art'),
    path('kategori_artikel',views.kategori,name='kategori_artikel'),
]