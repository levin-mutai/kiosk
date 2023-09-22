from celery import shared_task
from products.utils.notification import SMS


@shared_task(name="Send Message")
def send_sms(instance):
    SMS.send(
        instance.customer.phone_number,
        "A new order has been placed. Order ID : {}".format(instance.id),
    )
