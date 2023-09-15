from django.db import models
from django.urls import reverse
import uuid
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

User = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Customers_detail", kwargs={"pk": self.pk})

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField()
    image_url = models.CharField(max_length=2083, null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Products_detail", kwargs={"pk": self.pk})


class Order(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    ) 
    products = models.ManyToManyField(Product,through='OrderProduct',related_name="Orders")


    @property
    def total_price(self):
        """Used to dynamicaly to calculate the price of the order made"""
        return sum(x.total_price for x in self.products.all())
    def order_products(self):
        # Retrieve all OrderProduct objects related to this Order instance
        return OrderProduct.objects.filter(order=self)
    
class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        """Used to dynamicaly calculate the price of each order"""
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Order_Product"
        unique_together = ("order", "product")


    def get_absolute_url(self):
        return reverse("Orders_detail", kwargs={"pk": self.pk})