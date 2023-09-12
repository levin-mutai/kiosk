from celery import shared_task
from models import Order
from django.core.mail import send_mail  # Or use another method to send messages


@shared_task
def send_notification_task(order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Send your message here, for example, via email
        send_mail(
            "New Order Notification",
            f"New order placed: {order.product} x{order.quantity}",
            "sender@example.com",
            ["recipient@example.com"],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass
