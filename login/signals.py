from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, RDNWalletDetail

@receiver(post_save, sender=CustomUser)
def create_or_update_rdn_wallet(sender, instance, created, **kwargs):
    if created:  # Hanya saat user dibuat
        RDNWalletDetail.objects.create(
            user=instance,
            rdn=instance.rdn,
            balance=0
        )
    else:  # Saat user diperbarui
        wallet, _ = RDNWalletDetail.objects.get_or_create(user=instance)
        wallet.rdn = instance.rdn
        wallet.save()
