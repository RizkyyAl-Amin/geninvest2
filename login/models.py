from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    rdn = models.CharField(max_length=20, unique=True, null=True, blank=True)

class RDNWalletDetail(models.Model):
    rdn = models.CharField(max_length=20, unique=True)
    balance = models.BigIntegerField(default=0)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )

    def __str__(self):
        return f"RDN: {self.rdn} | Balance: {self.balance}"