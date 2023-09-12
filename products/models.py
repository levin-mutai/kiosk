from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Products_detail", kwargs={"pk": self.pk})


class Order(BaseModel):
    user_id = models.ForeignKey()  # TODO : add user Table
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        """Used to dynamicaly calculate the proce of the order made"""
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Orders_detail", kwargs={"pk": self.pk})
