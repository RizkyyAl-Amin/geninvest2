from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),

    path('artikel/', views.art, name='art'),
    path('artikel/create/', views.cartikel, name='cartikel'),
    path('artikel/edit/<int:pk>/', views.edit_artikel, name='edit_artikel'),
    path('artikel/delete/<int:pk>/', views.delete_artikel, name='delete_artikel'),
    path('kategori/', views.list_kategori, name='list_kategori'),
    path('kategori/create/', views.create_kategori, name='create_kategori'),
    path('kategori/delete/<int:pk>/', views.delete_kategori, name='delete_kategori'),


    path('produk/', views.list_produk, name='list_produk'),
    path('produk/create/', views.create_produk, name='create_produk'),
    path('produk/update/<int:pk>/', views.update_produk, name='update_produk'),
    path('produk/delete/<int:pk>/', views.delete_produk, name='delete_produk'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)