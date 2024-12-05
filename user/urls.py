from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('user_dashboard',views.u_dashboard,name='user_dashboard'),
    path('RDN_Wallet',views.wallet,name='wallet'),
    path('Portofolio',views.porto,name='porto'),
    path('Withdraw',views.jual,name='jual'),
    path('Deposit',views.beli,name='beli'),
]