from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Order, Product
from products.utils.notification import SMS
from django.core.cache import cache
from .tasks import send_sms


@receiver(post_save, sender=Order)
def order_saved_handler(sender, instance, created, **kwargs):
    """used to send a notification when an order is created"""
    if created:
        send_sms(instance)


@receiver(post_save, sender=Product)
def product_saved_handler(sender, instance, created, **kwargs):
    """used to invalidate the cache when a product is saved or deleted
    or when a product is added to an order
    """
    if created:
        cache.delete("product_list")
    elif instance.is_deleted:
        cache.delete("product_list")
