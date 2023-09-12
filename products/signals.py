from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Order
from products.utils.utils import send_order_notification


@receiver(post_save, sender=Order)
def order_saved_handler(sender, instance, created, **kwargs):
    if created:
        send_order_notification(instance.id)
